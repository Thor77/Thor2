import socket
import time
import sys
import plugins
import imp
import pkgutil
import inspect
from plugin import Plugin

class IRCBot:

    def __init__(self):
        # variables
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.debuglevel = 2 # 0 => nothing 1 => important messages 2 => everything
        self.realname = None # realname
        self.nick = None # nick
        self.server = None # server
        self.port = None # port
        self.call = None
        self.channel = None
        self.authpassword = None
        self.commands = {}
        self.eventlisteners = {}
        self.plugins = []
        self.loadedPlugins = []
        self.commandsByPlugin = {}
        #
        self.curr_channel = None

        # function calls

    # setter and getter
    def setDebugLevel(self, lvl):
        '''
        Set the debuglevel 0 => nothing 1 => important messages 2 => everything
        '''
        self.debuglevel = int(lvl)

    def getDebugLevel(self):
        '''
        get the debuglevel
        '''
        return self.debuglevel

    def setRealName(self, realname):
        '''
        set the realname
        '''
        self.realname = realname

    def getRealName(self):
        '''
        returns the realname
        '''
        return self.realname

    def setNick(self, nick):
        '''
        set the nick
        '''
        self.nick = nick

    def getNick(self):
        '''
        returns the nick
        '''
        return self.nick

    def setServer(self, server):
        '''
        set the server
        '''
        self.server = server

    def getServer(self):
        '''
        returns the server
        '''
        return self.server

    def setPort(self, port):
        '''
        set the port
        '''
        self.port = port

    def getPort(self):
        '''
        returns the port
        '''
        return self.port

    def setCall(self, call):
        '''
        set the call
        '''
        self.call = call

    def getCall(self):
        '''
        returns the call
        '''
        return self.call

    def setChannel(self, channel):
        '''
        set the channel
        '''
        self.channel = channel

    def getChannel(self):
        '''
        get the channel
        '''
        return self.channel

    def getCurrentChannel(self):
        '''
        returns a channel object of the current channel
        '''
        return self.curr_channel

    def setAuthPassword(self, password):
        '''
        set the authpassword (optional)
        '''
        self.authpassword = password

    def getAuthPassword(self):
        '''
        returns the auth password
        '''
        return self.authpassword

    # functions
    def connect(self):
        '''
        Connect to the irc-server
        '''
        if self.server != None and self.port != None:
            self.sock.connect((self.server, self.port))
            #self.sock.setblocking(False)
            self.debug('Connected to %s at port %i' % (self.server, self.port), 1)
        else:
            self.debug('Error connecting to server! No server and port set!', 1)
            sys.exit()

    def _send(self, line):
        '''
        Send line to the server
        '''
        self.debug('>>' + line, 2)
        self.sock.send((line + '\r\n').encode())

    #def _read(self):
        '''
        Read lines from the server
        '''
        """
        raw = self.sock.recv(4096).decode()
        raw = raw.strip()
        if len(raw) == 0:
            return []
        raw_lines = raw.split('\n')
        lines = []
        for line in raw_lines:
            lines.append(line)
            # debug
            self.debug('<<' + line, 2)
        return lines
        """
    def _read(self):
        b = ''
        data = True
        while data:
            raw = self.sock.recv(4096).decode()
            b += raw
            while b.find('\n') != -1:
                line, b = b.split('\n', 1)
                yield line
        return
        """
        lines = []
        raw = self.sock.recv(4096).decode()
        raw = raw.strip()
        if len(raw) == 0:
            return lines
        rawLines = raw.split('\r\n')
        for line in rawLines:
            msg = line.strip()
            lines.append(msg)
            self.debug('<<' + msg, 2)
        return lines
        """

    def debug(self, msg, lvl):
        '''
        Print debug-msg if debuglvl == msglvl
        '''
        if self.debuglevel >= lvl:
            print(msg)

    # commands
    def addCommand(self, trigger, function, helpstring, plugin):
        if not trigger in self.commands:
            self.commands[trigger.lower()] = [function, helpstring, plugin]
            if plugin in self.commandsByPlugin:
                self.commandsByPlugin[plugin].append(trigger)
            else:
                self.commandsByPlugin[plugin] = [trigger]

    def gotCommand(self, command, sender, args):
        if command in self.commands:
            try:
                self.commands[command][0](sender, args)
                self.debug('Executed %s!' % self.commands[command][0], 2)
            except:
                self.sendNotice('There was an error while executing your command!', sender)

    def deleteAllCommands(self):
        self.commands = {}
        self.commandsByPlugin = {}

    def deleteCommand(self, trigger):
        if trigger in self.commands:
            del self.commands[trigger]

    # events
    def registerEvent(self, eventname, function):
        if not eventname in self.eventlisteners:
            self.eventlisteners[eventname] = []
        a = self.eventlisteners[eventname]
        a.append(function)

    def gotEvent(self, eventname, eventobj):
        if eventname in self.eventlisteners:
            a = self.eventlisteners[eventname]
            for index, func in enumerate(a):
                a[index](eventobj)
                self.debug('"%s" executed by event "%s"!' % (func, eventname), 2)
        else:
            self.debug('No listener for event "%s"!' % eventname, 2)

    def unregisterEvent(self, eventname, function):
        if eventname in self.eventlisteners:
            a = self.eventlisteners[eventname]
            if function in a:
                a.remove(function)
    
    def unregisterAllEvents(self):
        self.eventlisteners = {}

    # plugins
    def unloadPlugins(self):
        self.deleteAllCommands()
        self.unregisterAllEvents()
        print(self.plugins)
        for plugin in self.plugins:
            plugin.unload()
        self.plugins = []
        self.loadedPlugins = []

    def loadPlugin(self, modname):
        module = __import__(modname, fromlist='dummy')
        imp.reload(module)
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, Plugin) and obj != Plugin:
                plugin = obj(self)
                self.plugins.append(plugin)
                self.loadedPlugins.append(modname.split('.')[-1])
                print('Loaded plugin ' + modname)
                print('Plugins: ' + ', '.join(self.loadedPlugins))

    def loadAllPlugins(self):
        prefix = plugins.__name__ + '.'
        for importer, modname, ispkg in pkgutil.iter_modules(plugins.__path__, prefix):
            del importer
            print('Loading %s' % modname)
            self.loadPlugin(modname)

    def reloadPlugins(self):
        print('Start reloading plugins...')
        self.unloadPlugins()
        print('Finished unloading plugins...')
        self.loadAllPlugins()
        print('Finished loading plugins...')
        print('Finished reloading plugins!')  

    # IRC-Functions
    def pong(self, ping):
        '''
        Send pong to the server
        '''
        self._send('PONG %s' % ping)

    def register(self):
        '''
        Send NICK and USER message to the server
        '''
        if self.nick != None and self.realname != None:
            self._send('NICK %s' % self.nick)
            self._send('USER {nick} {nick} {nick} :{realname}'.format(nick=self.nick, realname=self.realname))
            self.debug('Successfully registered as %s with realname %s!' % (self.nick, self.realname), 1)
        else:
            self.debug('Error registering! No nick or realname set!', 1)
            sys.exit()

    def sendMessage(self, message, reciever=None):
        '''
        Send message to channel
        '''
        if reciever == None:
            reciever = self.curr_channel
        self._send('PRIVMSG %s :%s' % (reciever, message))
        self.debug('<%s> %s' % (self.getNick(), message), 1)

    def sendNotice(self, message, nick):
        '''
        Send a notice to nick
        '''
        self._send('NOTICE %s :%s' % (nick, message))

    def join(self):
        '''
        join channel
        '''
        chan = self.channel
        if chan != None:
            # join channel
            self._send('JOIN %s' % chan)
            # set curr_channel
            self.curr_channel = chan
            # event
            eventobj = SelfJoinEvent(chan)
            self.gotEvent('onSelfJoin', eventobj)
            # debug
            self.debug('Joined channel %s!' % chan, 1)
        else:
            self.debug('ERROR: No channel set!', 1)
            sys.exit()

    def names(self, channel):
        '''
        send names-request to channel
        '''
        self._send('NAMES %s' % channel)

    def whois(self, nick):
        '''
        send whois-request to nick
        '''
        self._send('WHOIS %s' % nick)

    def quit(self, quitmsg='Bye!'):
        self.debug('Exit now!', 1)
        self._send('QUIT %s' % quitmsg)
        time.sleep(1)
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        sys.exit(0)

    def auth(self, nick, password):
        self._send('AUTH %s %s' % (nick, password))

    # Loop

    def start(self):
        #self.loadPlugins()
        self.connect()
        self.register()
        self.loadAllPlugins()
        if self.getCall() == None:
            self.debug('ERROR: No call set!', 1)
            sys.exit()
        # auth first
        if self.authpassword != None:
            self.auth(self.getNick(), self.getAuthPassword())
            self.debug('Successfully authed with nick %s!' % self.getNick(), 1)

        for line in self._read():
            #time.sleep(0.25) # wait
            self.debug('<<' + line, 2) # debug
            self._handleLine(line) # handle line

    def _handleLine(self, raw_line):
        # handle lines
        raw = Raw(self, raw_line)
        event = raw.getEvent()
        if event == 'PING':
            self.pong(raw.getMessage())
        elif event == '376' or event == '422':
            # End of MOTD or Missing MOTD
            self.join()
        elif event == 'PRIVMSG':
            msgobj = UserMessage(raw.getMessage(), raw.getSender().split('!')[0])
            # debug
            self.debug('<%s> %s' % (msgobj.getSender(), msgobj.getMessage()), 1)
            # run event
            eventobj = MessageEvent(msgobj.getSender(), msgobj.getMessage())
            self.gotEvent('onUserMessage', eventobj)
            # commands
            call = self.getCall()
            # look for command
            if msgobj.getMessage()[:(len(call))] == call:
                # call found
                self.debug('Found command!', 2)
                msg = msgobj.getMessage()
                msg_withoutcall = msg[len(call):]
                msg_withoutcall_split = msg_withoutcall.split(' ')
                cmd = msg_withoutcall_split[0]
                args = msg_withoutcall_split[1:]
                self.debug('Command: %s Arguments: %s' % (cmd, args), 2)
                self.gotCommand(cmd, msgobj.getSender(), args)
        elif event == 'JOIN':
            # join-msg
            joiner = raw.getSender().split('!')[0]
            if joiner != self.getNick():
                # event
                eventobj = UserJoinEvent(joiner)
                self.gotEvent('onUserJoin', eventobj)
                # debug
                self.debug('%s joined your channel!' % (joiner), 1)

class User:

    def __init__(self, bot, nick):
        self.nick = nick
        self.bot = bot

    def getNick(self):
        return self.nick

class UserMessage:

    def __init__(self, message, sender):
        self.message = message
        self.sender = sender

    def getMessage(self):
        return self.message

    def getSender(self):
        return self.sender

class Raw:

    def __init__(self, bot, raw):
        # set variables
        self.event = None
        self.sender = None
        self.target = None
        self.message = None
        #
        rawline = raw.strip()
        parts = rawline.split(' ')

        # check if ping
        if parts[0] == 'PING':
            # yes
            self.event = parts[0]
            self.message = parts[1][1:]
        elif parts[0][0] == ':':
            # no
            self.event = parts[1]
            self.sender = parts[0][1:]
            self.target = parts[2]
            if len(parts) > 2:
                parts = parts[3:]
                self.message = ' '.join(parts)[1:]

    def getEvent(self):
        return self.event

    def getSender(self):
        return self.sender

    def getTarget(self):
        return self.target

    def getMessage(self):
        return self.message

class MessageEvent:
    def __init__(self, user, message):
        self.user = user
        self.message = message

    def getMessage(self):
        return self.message

    def getSender(self):
        return self.user

class SelfJoinEvent:
    def __init__(self, channel):
        self.chan = channel

    def getChannel(self):
        return self.chan

class UserJoinEvent:
    def __init__(self, user):
        self.user = user

    def getUser(self):
        return self.user
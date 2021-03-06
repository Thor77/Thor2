import socket
import time
import sys
import plugins
import imp
import pkgutil
import inspect
from plugin import Plugin
import sqlite3
import re

class IRCBot:

    def __init__(self):
        # variables
        self.sock             = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.debuglevel       = 2 # 0 => nothing 1 => important messages 2 => everything
        self.realname         = None # realname
        self.nick             = None # nick
        self.server           = None # server
        self.port             = None # port
        self.call             = None
        self.channel          = None
        self.authpassword     = None
        self.commands         = {}
        self.eventlisteners   = {}
        self.plugins          = []
        self.loadedPlugins    = []
        self.commandsByPlugin = {}
        self.databasefile     = 'users.db'
        self.curr_channel     = None
        self.nickAuthnameDict = {}

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

    def setCurrentChannel(self, channel):
        '''
        set the current channel
        '''
        self.curr_channel = channel

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

    def setDatabaseFile(self, databasefile):
        self.databasefile = databasefile

    def getDatabaseFile(self):
        return self.databasefile

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
        line = re.sub(r'\s+', ' ', line)
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
            raw = self.sock.recv(4096).decode('UTF-8', 'ignore')
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
    def addCommand(self, trigger, function, helpstring, plugin, permissionlvl):
        if not trigger in self.commands:
            self.commands[trigger.lower()] = [function, helpstring, plugin, permissionlvl]
            if plugin in self.commandsByPlugin:
                self.commandsByPlugin[plugin].append(trigger)
            else:
                self.commandsByPlugin[plugin] = [trigger]

    def gotCommand(self, command, sender, args):
        command = command.lower()
        sender = sender.lower()
        authname = self.getAuthname(sender)
        if command in self.commands:
            if authname == None:
                self.sendNotice('You are not authed! Can\'t get your userlvl!', sender)
                return
            else:
                if not self.inDatabase(authname):
                    self.sendNotice('You are not in the database! Can\'t get your userlvl!', sender)
                    return
            senderlvl = self.getUserLevel(authname)
            neededlvl = self.commands[command][3]
            if senderlvl >= neededlvl:
                try:
                    self.commands[command][0](sender, args)
                    self.debug('Executed %s!' % self.commands[command][0], 2)
                except IndexError:
                    self.sendNotice('Too less arguments! Try %shelp %s for further information!' % (self.getCall(), command), sender)
                except Exception as e:
                    exception = '%s: %s' % (e.__class__.__name__, e.args[0])
                    self.debug(exception, 1)
                    self.sendNotice('ERROR: %s' % exception, sender)
            else:
                self.sendNotice('No permissions to use this command!', sender)
                self.sendNotice('You have level %s but you need level %s!' % (senderlvl, neededlvl), sender)

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
        self.debug(self.plugins, 2)
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
                self.debug('Loaded plugin ' + modname, 2)
                self.debug('Plugins: ' + ', '.join(self.loadedPlugins), 2)

    def loadAllPlugins(self):
        prefix = plugins.__name__ + '.'
        for importer, modname, ispkg in pkgutil.iter_modules(plugins.__path__, prefix):
            del importer
            self.debug('Loading %s' % modname, 2)
            self.loadPlugin(modname)

    def reloadPlugins(self):
        self.debug('Start reloading plugins...', 2)
        self.unloadPlugins()
        self.debug('Finished unloading plugins...', 2)
        self.loadAllPlugins()
        self.debug('Finished loading plugins...', 2)
        self.debug('Finished reloading plugins!', 2)

    # Permission
    def getUserLevel(self, nick):
        permissions = self.getPermissionsDict()
        if nick in permissions:
            return permissions[nick]
        else:
            return None

    def changeUserLevel(self, nick, newuserlvl):
        self.database_cursor.execute('UPDATE users SET lvl=? WHERE nick=?', (newuserlvl, nick))
        self.safeDatabase()

    def addUserToDatabase(self, nick):
        self.database_cursor.execute('INSERT INTO users VALUES (?, ?)', (str(nick).lower(), 0))
        self.debug('Successfully added "%s" to the database!' % nick, 2)
        self.safeDatabase()

    def getPermissionsDict(self):
        mydict = {}
        rows = self.database_cursor.execute('SELECT * FROM users ORDER BY lvl DESC')
        for nick, lvl in rows:
            mydict[nick] = lvl
        return mydict
        # read database
        # return dict {'nick' : permissionlvl} | {'thor77' : 2}
        # 2 => admin, 1 => moderator, 0 => none

    def deleteUser(self, nick):
        self.database_cursor.execute('DELETE FROM users WHERE nick=?', (nick.lower(),))
        self.safeDatabase()

    def connectDatabase(self, databfile):
        self.database = sqlite3.connect(databfile)
        self.database_cursor = self.database.cursor()
        self.database_cursor.execute('CREATE TABLE IF NOT EXISTS users (nick text, lvl integer)')

    def closeDatabase(self):
        self.safeDatabase()
        self.database.close()

    def safeDatabase(self):
        self.database.commit()

    def inDatabase(self, authname):
        usersdict = self.getPermissionsDict()
        if authname in usersdict:
            return True
        else:
            return False

    # add User
    def addUser(self, nick, authname):
        nick = nick.lower()
        authname = authname.lower()
        if authname != '0':
            if not nick in self.nickAuthnameDict:
                self.nickAuthnameDict[nick] = authname
            if not self.inDatabase(authname):
                self.addUserToDatabase(authname)

    def getAuthname(self, nick):
        nick = nick.lower()
        if nick in self.nickAuthnameDict:
            return self.nickAuthnameDict[nick]
        else:
            return None

    def getUserNick(self, authname):
        authname = authname.lower()
        authnameUserDict = {v:k for k, v in self.nickAuthnameDict.items()}
        if authname in authnameUserDict:
            return authnameUserDict[authname]
        else:
            return None

    def changeUserNick(self, oldnick, newnick):
        oldnick = oldnick.lower()
        newnick = newnick.lower()
        if oldnick in self.nickAuthnameDict:
            self.nickAuthnameDict[newnick] = self.nickAuthnameDict[oldnick]
            del self.nickAuthnameDict[oldnick]

    # IRC-Functions
    def pong(self, ping):
        '''
        Send pong to the server
        '''
        self._send('PONG :%s' % ping)

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
            reciever = self.getCurrentChannel()
        self._send('PRIVMSG %s :%s' % (reciever, message))
        self.debug('<%s> %s' % (self.getNick(), message), 1)

    def sendNotice(self, message, nick):
        '''
        Send a notice to nick
        '''
        self._send('NOTICE %s :%s' % (nick, message))

    def join(self, channel=None):
        '''
        join channel
        '''
        if channel != None:
            chan = channel
        elif self.channel != None:
            chan = self.channel
        else:
            self.debug('ERROR: No channel set!', 1)
            sys.exit()
        # join channel
        self._send('JOIN %s' % chan)
        # set curr_channel
        self.setCurrentChannel(chan)
        # event
        eventobj = SelfJoinEvent(chan)
        self.gotEvent('onSelfJoin', eventobj)
        # debug
        self.debug('Joined channel %s!' % chan, 1)
        # users in channel
        self.debug('Will now send NickRequest!', 2)
        self.whoChannelUsers()

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
        self.unloadPlugins()
        self.debug('Exit now!', 1)
        self._send('QUIT :%s' % quitmsg)
        time.sleep(1)
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        self.closeDatabase()
        sys.exit(0)

    def auth(self, nick, password):
        self._send('AUTH %s %s' % (nick, password))

    def kick(self, nick, reason=None):
        if reason != None:
            self._send('KICK %s %s :%s' % (self.getCurrentChannel(), nick, reason))
        else:
            self._send('KICK %s %s' % (self.getCurrentChannel(), nick))

    def part(self, channel=None):
        if channel == None:
            channel = self.getCurrentChannel()
        self._send('PART %s' % channel)

    def changeChannel(self, changeTo):
        self.part()
        self.join(changeTo)

    def whoChannelUsers(self, channel=None):
        if channel == None:
            channel = self.getCurrentChannel()
        self._send('WHO %s c%%nuhar' % channel)

    def changeNick(self, newnick):
        self._send('NICK %s' % newnick)

    # modes
    def op(self, nick):
        self._send('MODE %s +o %s' % (self.getCurrentChannel(), nick))

    def deop(self, nick):
        self._send('MODE %s -o %s' % (self.getCurrentChannel(), nick))

    def voice(self, nick):
        self._send('MODE %s +v %s' % (self.getCurrentChannel(), nick))

    def devoice(self, nick):
        self._send('MODE %s -v %s' % (self.getCurrentChannel(), nick))

    # Loop

    def start(self):
        #self.loadPlugins()
        self.connect()
        self.register()
        self.loadAllPlugins()
        self.connectDatabase(self.getDatabaseFile())
        if self.getCall() == None:
            self.debug('ERROR: No call set!', 1)
            sys.exit()
        try:
            for line in self._read():
                    #time.sleep(0.25) # wait
                    self.debug('<<' + line, 2) # debug
                    self._handleLine(line) # handle line
        except KeyboardInterrupt:
            self.quit()

    def _handleLine(self, raw_line):
        # handle lines
        raw = Raw(self, raw_line)
        event = raw.getEvent()
        if event == 'PING':
            self.pong(raw.getMessage())
        elif event == '376' or event == '422':
            # End of MOTD or Missing MOTD
            # auth first
            if self.authpassword != None:
                self.auth(self.getNick(), self.getAuthPassword())
                self.debug('Successfully authed with nick %s!' % self.getNick(), 1)
            # join
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
                #
                self.whoChannelUsers()
        elif event == 'PART' or event == 'QUIT':
            quituser = raw.getSender().split('!')[0]
            if quituser != self.getNick():
                # event
                eventobj = UserQuitEvent(quituser)
                self.gotEvent('onUserQuit', eventobj)
                # debug
                self.debug('%s parted from your channel!' % quituser, 1)
        elif event == 'NICK':
            oldnick = raw.getSender().split('!')[0]
            self.debug('Found old nick: %s' % oldnick, 2)
            newnick = raw.getTarget()[1:]
            self.debug('Found new nick: %s' % newnick, 2)
            # event
            eventobj = UserNickChange(oldnick, newnick)
            self.gotEvent('onUserNickChange', eventobj)
            # edit user
            self.changeUserNick(oldnick, newnick)
        elif event == '354':
            #  WHO #channel c%nuhar
            information = raw.getMessage().split(' ')
            nick = information[2]
            #self.debug('Found nick: %s' % nick, 2)
            authname = information[3]
            #self.debug('Found authname: %s' % authname, 2)
            self.addUser(nick, authname)

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
        else:
            self.message = ' '.join(parts)

    def getEvent(self):
        return self.event

    def getSender(self):
        return self.sender

    def getTarget(self):
        return self.target

    def getMessage(self):
        return self.message

# Events
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

class  UserQuitEvent:
    def __init__(self, user):
        self.user = user

    def getUser(self):
        return self.user

class UserNickChange:
    def __init__(self, oldnick, newnick):
        self.oldnick = oldnick
        self.newnick = newnick

    def getOldNick(self):
        return self.oldnick

    def getNewNick(self):
        return self.newnick
import socket
import time
import sys

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

    def getChannel(self, channel):
        '''
        get the channel
        '''
        return self.channel

    def getCurrentChannel(self, channel):
        '''
        returns a channel object of the current channel
        '''
        return self.curr_channel

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

    def sendMessage(self, channel, message):
        '''
        Send message to channel
        '''
        self._send('PRIVMSG %s :%s' % (channel.getName(), message))

    def sendNotice(self, nick, message):
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
            # create channel object
            self.curr_channel = Channel(self, chan)
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
        time.sleep(0.5)
        self._send('QUIT %s' % quitmsg)
        sys.exit()

    # Loop

    def start(self):
        #self.loadPlugins()
        self.connect()
        self.register()
        if self.getCall() == None:
            self.debug('ERROR: No call set!', 1)
            sys.exit()
        for line in self._read():
            #time.sleep(0.25) # wait
            self.debug('<<' + line, 2) # debug
            self._handleLine(line) # handle line

    def _handleLine(self, raw_line):
        raw = Raw(self, raw_line)
        event = raw.getEvent()
        if event == 'PING':
            self.pong(raw.getMessage())
        elif event == '376' or event == '422':
            # End of MOTD
            self.join()
        elif event == 'PRIVMSG':
            msg = raw.getMessage()
            sender = raw.getSender().split('!')[0]
            if msg == '!q':
                self.quit()
            self.debug('<%s> %s' % (sender, msg), 1)
        elif event == 'JOIN':
            # join-msg
            joiner = raw.getSender().split('!')[0]
            self.debug('%s joined your channel!' % (joiner), 1)

class Channel:

    def __init__(self, bot, name):
        self.channelname = name
        self.bot = bot

    def getName(self):
        return self.channelname

    def getUsers(self):
        #self.bot.names(self.getName())
        pass

class User:

    def __init__(self, bot, nick):
        self.nick = nick
        self.bot = bot

    def getNick(self):
        return self.nick

class UserMessage:

    def __init__(self, msg):
        self.message = message

    def getMessage(self):
        return self.message

    def getSender(self):
        pass

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
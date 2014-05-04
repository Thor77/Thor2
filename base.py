import socket
import time

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
            self.debug('Connected to %s at port %i' % (self.server, self.port), 1)
        else:
            self.debug('Error connecting to server! No server and port set!', 1)

    def _send(self, line):
        '''
        Send line to the server
        '''
        self.debug('>>' + line, 2)
        self.sock.send((line + '\r\n').encode())

    def _read(self):
        '''
        Read lines from the server
        '''
        raw = self.sock.recv(1024).decode()
        raw = raw.strip()
        raw_lines = raw.split('\n')
        lines = []
        for line in raw_lines:
            lines.append(line)
            # debug
            self.debug('<<' + line, 2)
        return lines

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
            self.curr_channel = Channel(chan)
        else:
            self.debug('Joined channel %s!' % self.channel, 1)

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

    # Loop

    def start(self):
        #self.loadPlugins()
        self.connect()
        self.register()
        if self.getCall() == None:
            return
        while True:
            time.sleep(0.25)
            lines = self._read()
            for line in lines:
                self._handleLine(line)

    def _handleLine(self, raw_line):
        raw = Raw(self, raw_line)

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
        self.raw = raw
        self.bot = bot
        rawline = raw.strip()
        parts = rawline.split()

    def getType(self):
        pass
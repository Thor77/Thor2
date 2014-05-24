Thor2
=====

My IRC-Bot named Thor2

START HERE
==========
## The init-File
    from base import IRCBot
    
    bot = IRCBot()
    bot.setServer('irc.quakenet.org') # the irc-server
    bot.setPort(6667) # port of the server
    bot.setRealname('Realname') # realname of the bot
    bot.setNick('Nick') # nick of the bot
    bot.setCall('>') # char to call the bot
    bot.setChannel('#mychannel') # channel to join after connect
    bot.setDebugLevel(1) #  0 => nothing 1 => important messages (recommend) 2 => everyhthing
    bot.start() # start the bot
    
## Sample Plugin
Place your plugin in the plugins-folder, it will be load automatically at startup.
You can reload plugins using the reload-command!
    from plugin import Plugin
    
    class MyPlugin(Plugin):
        def onLoad(self):
            # called on load
            # register events and add commands here
            self.addCommand('mytestcommand', self.mytestcommand_func, 'a simple test command', 0)
            # cmd, function, helpstring, needed level
            
            # for a eventlist look down here
            self.registerEvent('onUserMessage', self.onMessage)
            
        def onMessage(self, eventobj):
            msg = eventobj.getMessage()
            sender = eventobj.getSender()
            
        def mytestcommand_func(self, sender, args):
            # sender: sender of the message
            # dict with args (everything after the command)
            # mytestcommand thor77
            nick = args[0] # thor77
            self.sendMessage('Hi %s!' % nick) # Hi thor77!

Events
======
## onUserMessage
### Methods
    getMessage  
    getSender
## onSelfJoin
### Methods
    getChannel
## onUserJoin
### Methods
    getUser
## onUserQuit
### Methods
    getUser

TODO
====
- unload Plugins through a command
- load Plugins through a command
- Permission System | DONE

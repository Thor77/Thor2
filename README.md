Thor2
=====

My IRC-Bot named Thor2

START HERE
==========
## The bot.cfg-File
    
    [Server]
    ip         = irc.quakenet.org # ip of the irc-server
    port       = 6667 # port of the irc-server

    [IRC]
    realname   = Thor2 # realname of the bot
    nick       = Thor2 # nick of the bot

    [Bot]
    call       = $ # char the bot will wait for ($help)
    channel    = #thorsraum # channel to join
    debuglevel = 0 # debuglvl | 0 => nothing 1 => important messages 2 => everything

### Set Auth-Password
Append this line to the __init__.py:
    bot.setAuthPassword('pw') # set the auth password to 'pw'
    
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

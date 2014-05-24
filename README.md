Thor2
=====

My IRC-Bot named Thor2

START HERE
==========
## The __init__-File
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

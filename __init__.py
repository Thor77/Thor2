from base import IRCBot
import configparser

config = configparser.ConfigParser()
config.read('bot.cfg')

server = config.get('Server', 'ip')
port = config.getint('Server', 'port')
realname = config.get('IRC', 'realname')
nick = config.get('IRC', 'nick')
call = config.get('Bot', 'call')
channel = config.get('Bot', 'channel')
debuglvl = config.getint('Bot', 'debuglevel')

bot = IRCBot()
bot.setServer(server)
bot.setPort(port)
bot.setRealName(realname)
bot.setNick(nick)
bot.setCall(call)
bot.setChannel(channel)
bot.setDebugLevel(debuglvl)
bot.start()
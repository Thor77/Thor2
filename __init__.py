from base import IRCBot

bot = IRCBot()
bot.setServer('irc.quakenet.org')
bot.setPort(6667)
bot.setRealName('Thor22')
bot.setNick('Thor22')
bot.setCall('$')
bot.setDebugLevel(2)
bot.start()
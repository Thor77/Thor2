from base import IRCBot

bot = IRCBot()
bot.setServer('irc.quakenet.org')
bot.setPort(6667)
bot.setRealName('Thor2')
bot.setNick('Thor22')
bot.setCall('$')
bot.setChannel('#thorsraum')
bot.setDebugLevel(1)
bot.start()
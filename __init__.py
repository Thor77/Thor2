from base import IRCBot

bot = IRCBot()
bot.setServer('irc.theradio.cc')
bot.setPort(6667)
bot.setRealName('Thor2')
bot.setNick('Thor2')
bot.setCall('$')
bot.setChannel('#kindergarten')
bot.setDebugLevel(0)
bot.start()
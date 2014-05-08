from plugin import Plugin

class Greet(Plugin):

	def onLoad(self):
		# commands

		# events
		self.registerEvent('onUserJoin', self.onUserJoin)
		self.registerEvent('onSelfJoin', self.onSelfJoin)

	def onUserJoin(self, eventobj):
		joiner = eventobj.User()
		self.sendMessage('Herzlich Willkommen %s! Du bist hier in %s.' % (joiner, self.sock.getChannel))

	def onSelfJoin(self, eventobj):
		self.sendMessage('So, ich bin dann auch mal da...')
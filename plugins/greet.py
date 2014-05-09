from plugin import Plugin

class Greet(Plugin):

	def onLoad(self):
		self.greet = True
		# commands
		self.addCommand('dgreet', self.dgreet_func, 'Disable greeting new users')
		self.addCommand('egreet', self.egreet_func, 'Enable greeting new users')
		self.addCommand('gstatus', self.gstatus_func, 'Show the greeting status')
		# events
		self.registerEvent('onUserJoin', self.onUserJoin)
		self.registerEvent('onSelfJoin', self.onSelfJoin)

	def onUserJoin(self, eventobj):
		if self.greet:
			joiner = eventobj.getUser()
			self.sendMessage('Herzlich Willkommen %s! Du bist hier in %s.' % (joiner, self.sock.getCurrentChannel()))

	def onSelfJoin(self, eventobj):
		self.sendMessage('So, ich bin dann auch mal da...')

	def dgreet_func(self, sender, args):
		if not self.greet:
			self.sendNotice('Greeting already disabled!', sender)
		else:
			self.greet = False
			self.sendMessage('Greeting disabled!')

	def egreet_func(self, sender, args):
		if self.greet:
			self.sendNotice('Greeting already enabled!', sender)
		else:
			self.greet = True
			self.sendMessage('Greeting enabled!')

	def gstatus_func(self, sender, args):
		if self.greet:
			status = 'enabled'
		else:
			status = 'disabled'
		self.sendNotice('Greeting is %s!' % status, sender)
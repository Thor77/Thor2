from plugin import Plugin

class Greet(Plugin):

	def onLoad(self):
		self.greet = False
		# commands
		self.addCommand('dgreet', self.dgreet_func, 'Disable greeting new users', 1)
		self.addCommand('egreet', self.egreet_func, 'Enable greeting new users', 2)
		self.addCommand('gstatus', self.gstatus_func, 'Show the greeting status', 1)
		# events
		self.registerEvent('onUserJoin', self.onUserJoin)
		self.registerEvent('onSelfJoin', self.onSelfJoin)
		self.registerEvent('onUserQuit', self.onUserQuit)

	def onUserJoin(self, eventobj):
		if self.greet:
			joiner = eventobj.getUser()
			self.sendMessage('Herzlich Willkommen %s! Du bist hier in %s.' % (joiner, self.sock.getCurrentChannel()))

	def onSelfJoin(self, eventobj):
		self.sendMessage('So, ich bin dann auch mal da...')

	def onUserQuit(self, eventobj):
		if self.greet:
			quituser = eventobj.getUser()

	def dgreet_func(self, sender, args):
		if not self.greet:
			self.sendNotice('Greeting already disabled!', sender)
		else:
			self.greet = False
			self.sendNotice('Greeting disabled!', sender)

	def egreet_func(self, sender, args):
		if self.greet:
			self.sendNotice('Greeting already enabled!', sender)
		else:
			self.greet = True
			self.sendNotice('Greeting enabled!', sender)

	def gstatus_func(self, sender, args):
		if self.greet:
			status = 'enabled'
		else:
			status = 'disabled'
		self.sendNotice('Greeting is %s!' % status, sender)
from plugin import Plugin
import threading

class TheRadioCC(Plugin):

	def onLoad(self):
		self.np_announce = False
		# commands
		self.addCommand('eannounce', self.eannounce_func, 'enable NP-Announcing')
		self.addCommand('dannounce', self.dannounce_func, 'disable NP-Announcing')

	def eannounce_func(self, sender, args):
		self.np_announce = True
		self.sendNotice('NP-Announcing enabled!', sender)

	def dannounce_func(self, sender, args):
		self.np_announce = False
		self.sendNotice('NP-Announcing disabled!', sender)
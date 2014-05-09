from plugin import Plugin
import threading
import requests

class TheRadioCC(Plugin):

	def onLoad(self):
		self.np_announce = False
		self.curr_song = None
		# commands
		self.addCommand('eannounce', self.eannounce_func, 'enable NP-Announcing')
		self.addCommand('dannounce', self.dannounce_func, 'disable NP-Announcing')
		# start timer
		t = threading.Timer(5, self.announce)
		t.daemon = True
		t.start()
		self.debug('Timer started!', 2)

	def eannounce_func(self, sender, args):
		self.np_announce = True
		self.sendNotice('NP-Announcing enabled!', sender)

	def dannounce_func(self, sender, args):
		self.np_announce = False
		self.sendNotice('NP-Announcing disabled!', sender)

	def announce(self):
		current = requests.get('http://theradio.cc:12011').text
		# check if changed
		if self.curr_song != current:
			# yes
			self.curr_song = current
			if self.np_announce:
				# announcte
				self.debug('Announcing...', 1)
				self.sendMessage(current)
		threading.Timer(10, self.announce).start()
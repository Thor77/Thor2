from plugin import Plugin
import threading
import requests

class TheRadioCC(Plugin):

	def onLoad(self):
		self.np_announce = False
		self.curr_song = None
		# commands
		self.addCommand('eannounce', self.eannounce_func, 'enable NP-Announcing', 1)
		self.addCommand('dannounce', self.dannounce_func, 'disable NP-Announcing', 1)
		self.addCommand('np', self.np_func, 'show the now playing song on TheRadioCC')
		# start timer
		t = threading.Timer(10, self.announce)
		t.daemon = True
		t.start()
		self.debug('Trcc-Announce-Timer started!', 2)

	def np_func(self, sender, args):
		current = requests.get('http://theradio.cc:12011').text
		self.sendMessage(current)

	def eannounce_func(self, sender, args):
		if not self.np_announce:
			self.np_announce = True
			self.sendNotice('NP-Announcing enabled!', sender)
			self.startNextTimer()
		else:
			self.sendNotice('NP-Announcing already enabled!', sender)

	def dannounce_func(self, sender, args):
		if self.np_announce:
			self.np_announce = False
			self.sendNotice('NP-Announcing disabled!', sender)
		else:
			self.sendNotice('NP-Announcing already disabled!', sender)

	def announce(self):
		# get current song
		current = requests.get('http://theradio.cc:12011').text
		# check if changed
		if self.curr_song != current:
			# yes
			self.curr_song = current
			if self.np_announce:
				# announcte
				self.debug('Announcing...', 1)
				self.sendMessage(current)
				self.startNextTimer()

	def startNextTimer(self):
		timer = threading.Timer(10, self.announce)
		timer.start()
		self.debug('Next timer started!', 2)

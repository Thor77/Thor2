from plugin import Plugin
from bs4 import BeautifulSoup
import urllib.request

class Horoskop(Plugin):

    def onLoad(self):
        self.mode = 0 # 0 => only first sentence | 1 => complete
        self.asterisks = ['widder', 'stier', 'zwilling', 'krebs', 'löwe', 'jungrau', 'waage', 'skorpion', 'schütze', 'steinbock', 'wassermann', 'fische']
        # commands
        self.addCommand('horoSwitch', self.horoSwitch_cmd, 'Switch mode (only first sentence | complete)', 1)
        self.addCommand('horoMode', self.horoMode_cmd, 'Show mode')
        self.addCommand('horoskop', self.horoskop_cmd, 'horoskop <asterisk> | show horoskop for <asterisk>')

    def horoSwitch_cmd(self, sender, args):
        if self.mode == 1:
            self.mode = 0
        else:
            self.mode = 1
        self.sendNotice('Successfully changed mode to %s!' % self.mode, sender)

    def horoMode_cmd(self, sender, args):
        i_mode = {0: 'only first sentence', 1: 'complete'}
        self.sendNotice('Mode is set to "%s"!' % i_mode[self.mode], sender)

    def horoskop_cmd(self, sender, args):
        asterisk = args[0].lower()
        if asterisk in self.asterisks:
            horo = self.get_horoskop(asterisk)
            self.sendMessage('Horoscope for %s:' % asterisk)
            if self.mode == 0:
                self.sendMessage(horo.split('.')[0])
            else:
                self.sendMessage(horo)
        else:
            self.sendNotice('Invalid asterisk!', sender)

    def get_horoskop(self, asterisk):
        y_url = 'https://de.horoskop.yahoo.com/horoskop/'
        url =  y_url + asterisk + '/'
        soup = BeautifulSoup(urllib.request.urlopen(url))
        x = soup.find('div', attrs={'class': 'astro-tab-body'})
        return x.p.text
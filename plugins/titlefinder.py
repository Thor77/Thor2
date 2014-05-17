from plugin import Plugin
try:
    from bs4 import BeautifulSoup
    import urllib2
    bs_avail = True
except ImportError:
    bs_avail = False

class TitleFinder(Plugin):
    
    def onLoad(self):
        if bs_avail:
            # commands
            self.addCommand('eTitleFinder', self.eTitleFinder_func, 'enables the TitleFinder', 1)
            self.addCommand('dTitleFinder', self.dTitleFinder_func, 'disables the TitleFinder', 1)
            # events
            self.registerEvent('onUserMessage', self.onMessage)
            #

    def onMessage(self, eventobj):
        msg = eventobj.getMessage()

    def eTitleFinder_func(self, sender, args):
        pass

    def dTitleFinder_func(self, sender, args):
        pass

    def getTitle(self, url):
        soup = BeautifulSoup(urllib2.urlopen(url))
        return soup.title.string
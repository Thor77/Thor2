from plugin import Plugin
try:
    from bs4 import BeautifulSoup
    import urllib.request
    import urllib.error
    import re
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
            self.TitleFinderEnabled = False
        else:
            self.debug('TitleFinder plugin not available! Install BeautifulSoup!', 1)

    def onMessage(self, eventobj):
        if not self.TitleFinderEnabled:
            return
        msg = eventobj.getMessage()
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', msg)
        if len(urls) != 0:
            for url in urls:
                title = self.getTitle(url)
                if title != None:
                    self.sendMessage('Title: %s' % title)

    def eTitleFinder_func(self, sender, args):
        if not self.TitleFinderEnabled:
            self.TitleFinderEnabled = True
            self.sendNotice('TitleFinder enabled!', sender)
        else:
            self.sendNotice('TitleFinder already enabled!', sender)

    def dTitleFinder_func(self, sender, args):
        if self.TitleFinderEnabled:
            self.TitleFinderEnabled = False
            self.sendNotice('TitleFinder disabled!', sender)
        else:
            self.sendNotice('TitleFinder already disabled!', sender)

    def getTitle(self, url):
        try:
            soup = BeautifulSoup(urllib.request.urlopen(url))
            if soup.find('html') == None:
                self.debug('TitleFinder: No html!', 1)
                return None
            else:
                return soup.title.string
        except urllib.error.HTTPError as e:
            self.debug('TitleFinder: HTTPError %s while finding title!' % e.code, 1)
        except:
            self.debug('TitleFinder: ERROR finding title!', 1)
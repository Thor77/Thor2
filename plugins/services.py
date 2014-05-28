from plugin import Plugin
import requests
import urllib.parse

class Services(Plugin):

    def onLoad(self):
        # commands
        self.addCommand('google', self.google_func, 'google <searchstring> | search for <searchstring> on google')
        self.addCommand('googleLink', self.googleLink_func, 'googleLink <searchstring> | get the link to the search for <searchstring>')
        self.addCommand('lmgtfy', self.lmgtfy_func, 'lmgtfy <searchstring> | get the link to the lmgtfy for <searchstring>')

    def google_func(self, sender, args):
        search_string = ' '.join(args)
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&hl=de&q=' + urllib.parse.quote(search_string)
        r = requests.get(url)
        data = r.json()
        firstresult = data['responseData']['results'][0]
        self.sendMessage('%s - %s' % (firstresult['titleNoFormatting'], firstresult['url']))

    def googleLink_func(self, sender, args):
        link = 'https://www.google.com/#q=' + args.join('+')
        self.sendMessage(link)

    def lmgtfy_func(self, sender, args):
        link = 'http://lmgtfy.com/?q=' + args.join('+')
        self.sendMessage(link)
from plugin import Plugin
from twython import Twython
import threading

class Twitter(Plugin):

    def onLoad(self):
        self.enabled = False
        self.delay = 60
        self.hashtag = '#esc'
        consumer_key    = 'kzrUWTG08A5aIjO6IJjuA'
        consumer_secret = '5ivJzkNJGrrSmq6FliYKfZiZIpXROoU9SH5neO52ebw'
        access_key      = '2338381512-c1y1OR6ClMt24NaENdJqZuNCZtO4VqA9MqQdQuf'
        access_secret   = 'YFTUmQLmwz9fLW0zT9L36Vv2kqHnGwaeHhvBCklE4F28G'
        self.t = Twython(consumer_key, consumer_secret, access_key, access_secret)
        # commands
        self.addCommand('eTwitter', self.enableTwitter_func, 'enable Twitter-Tweet-sending')
        self.addCommand('dTwitter', self.disableTwitter_func, 'disable Twitter-Tweet-sending')
        self.addCommand('setHashtag', self.setHashtag_func, 'setHashtag <hashtag> | set hashtag to get reulsts from')
        self.addCommand('showHashtag', self.showHashtag_func, 'show the current hashtag')
        self.addCommand('setDelay', self.setDelay_func, 'setDelay <delay> | set delay between messages')
        self.addCommand('showDelay', self.showDelay_func, 'show the delay')

    def enableTwitter_func(self, sender, args):
        self.enabled = True
        self.sendTweet()
        self.sendNotice('Enabled!', sender)

    def disableTwitter_func(self, sender, args):
        self.enabled = False
        self.sendNotice('Disabled!', sender)

    def setDelay_func(self, sender, args):
        newdelay = args[0]
        self.delay = int(newdelay)

    def setHashtag_func(self, sender, args):
        self.hashtag = '#' + args[0]

    def showHashtag_func(self, sender, args):
        self.sendMessage('Current Hashtag: %s' % self.hashtag)

    def showDelay_func(self, sender, args):
        self.sendMessage('Current delay: ' % self.delay)

    def sendTweet(self):
        tweet = self.t.search(q=self.hashtag, result_type='recent')['statuses'][0]['text']
        self.sendMessage(tweet)
        if self.enabled:
            threading.Timer(self.delay, self.sendTweet).start()
from plugin import Plugin
from twython import Twython
import threading

class Esc(Plugin):

    def onLoad(self):
        self.enabled = False
        consumer_key    = 'kzrUWTG08A5aIjO6IJjuA'
        consumer_secret = '5ivJzkNJGrrSmq6FliYKfZiZIpXROoU9SH5neO52ebw'
        access_key      = '2338381512-c1y1OR6ClMt24NaENdJqZuNCZtO4VqA9MqQdQuf'
        access_secret   = 'YFTUmQLmwz9fLW0zT9L36Vv2kqHnGwaeHhvBCklE4F28G'
        self.t = Twython(consumer_key, consumer_secret, access_key, access_secret)
        # commands
        self.addCommand('eTwitter', self.enableTwitter_func, '')
        self.addCommand('dTwitter', self.disableTwitter_func, '')

    def enableTwitter_func(self, sender, args):
        self.enabled = True
        self.sendTweet()
        self.sendNotice('Enabled!', sender)

    def disableTwitter_func(self, sender, args):
        self.enabled = False
        self.sendNotice('Disabled!', sender)

    def sendTweet(self):
        tweet = self.t.search(q='#esc', result_type='recent')['statuses'][0]['text']
        self.sendMessage(tweet)
        if self.enabled:
            threading.Timer(10, self.sendTweet).start()
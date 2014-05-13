from plugin import Plugin
from twython import Twython
from threading import Thread
from threading import Event

class Twitter(Plugin):

    def onLoad(self):
        self.enabled    = False
        self.hashtag    = '#esc'
        self.lastTweet  = None
        self.startdelay = 20
        consumer_key    = 'kzrUWTG08A5aIjO6IJjuA'
        consumer_secret = '5ivJzkNJGrrSmq6FliYKfZiZIpXROoU9SH5neO52ebw'
        access_key      = '2338381512-c1y1OR6ClMt24NaENdJqZuNCZtO4VqA9MqQdQuf'
        access_secret   = 'YFTUmQLmwz9fLW0zT9L36Vv2kqHnGwaeHhvBCklE4F28G'
        self.t          = Twython(consumer_key, consumer_secret, access_key, access_secret)
        # commands
        self.addCommand('eTwitter', self.enableTwitter_func, 'enable Twitter-Tweet-sending')
        self.addCommand('dTwitter', self.disableTwitter_func, 'disable Twitter-Tweet-sending')
        self.addCommand('setSearch', self.setSearch_func, 'setSearch <searchstring> | set search to get reulsts from')
        self.addCommand('showSearch', self.showSearch_func, 'show the current searchstring')
        self.addCommand('setDelay', self.setDelay_func, 'setDelay <delay> | set delay between messages')
        self.addCommand('showDelay', self.showDelay_func, 'show the delay')
        # init Thread
        self.resetThread()

    def resetThread(self):
        self.stopFlag = Event()
        self.thread = MyThread(self.stopFlag, self.sendTweet, self.startdelay)

    def enableTwitter_func(self, sender, args):
        if self.enabled:
            self.sendNotice('Already enabled!', sender)
            return
        self.enabled = True
        self.sendNotice('Enabled!', sender)
        self.thread.start()

    def disableTwitter_func(self, sender, args):
        if not self.enabled:
            self.sendNotice('Already disabled!', sender)
            return
        self.enabled = False
        self.stopFlag.set()
        self.resetThread()
        self.sendNotice('Disabled!', sender)

    def setDelay_func(self, sender, args):
        newdelay = int(args[0])
        self.thread.changeDelay(newdelay)
        self.sendNotice('Delay set to %s!' % newdelay, sender)

    def setSearch_func(self, sender, args):
        self.search = args[0]
        self.sendNotice('Searchstring set to %s!' % self.search, sender)

    def showSearch_func(self, sender, args):
        self.sendMessage('Current Searchstring: %s' % self.search)

    def showDelay_func(self, sender, args):
        self.sendMessage('Current delay: %s' % self.thread.getDelay())

    def sendTweet(self):
        tweet = self.t.search(q=self.search, result_type='recent')['statuses'][0]['text']
        if tweet != self.lastTweet:
            self.lastTweet = tweet
            self.sendMessage(tweet)

class MyThread(Thread):
    def __init__(self, event, function, delay):
        Thread.__init__(self)
        self.stopped = event
        self.function = function
        self.delay = delay

    def run(self):
        while not self.stopped.wait(self.delay):
            self.function()
            print('Executed function!')

    def changeDelay(self, newdelay):
        self.delay = newdelay

    def getDelay(self):
        return self.delay
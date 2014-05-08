import inspect
import time
class Plugin:
    def __init__(self, sock):
        self.sock = sock
        self.messageDelay = 1
        if hasattr(self, 'onLoad') and inspect.ismethod(getattr(self, 'onLoad')):
            self.onLoad()

    def addCommand(self, trigger, function, helpstring):
        self.sock.addCommand(trigger, function, helpstring, self.getName())

    def sendMessage(self, message, reciever=None):
        self.sock.sendMessage(message, reciever)
        time.sleep(self.messageDelay)

    def sendNotice(self, notice, nick):
        self.sock.sendNotice(notice, nick)

    def debug(self, msg, debuglvl):
        self.sock.debug(msg, debuglvl)

    def registerEvent(self, eventname, function):
        self.sock.registerEvent(eventname, function)

    def unregisterEvent(self, eventname, function):
        self.sock.unregisterEvent(eventname, function)

    def unload(self):
        self.debug('Plugin %s unloaded!' % self.getName(), 2)

    def getName(self):
        return self.__class__.__name__
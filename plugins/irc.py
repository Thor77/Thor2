from plugin import Plugin

class IRC(Plugin):

    def onLoad(self):
        # commands
        self.addCommand('op', self.op_func, 'op <nick> | give <nick> op rights')
        self.addCommand('deop', self.deop_func, 'deop <nick> | remove <nick>s op rights')
        self.addCommand('voice', self.voice_func, 'voice <nick> | allow <nick> to speak')
        self.addCommand('devoice', self.devoice_func, 'devoice <nick> | deny <nick> to speak')

    def op_func(self, sender, args):
        nick = args[0]
        self.sock.op(nick)
        self.sendMessage('%s hat hier jetzt OP-Rechte!' % nick)

    def deop_func(self, sender, args):
        nick = args[0]
        self.sock.deop(nick)
        self.sendMessage('%s hat hier keine OP-Rechte mehr!' % nick)

    def voice_func(self, sender, args):
        nick = args[0]
        self.sock.voice(nick)
        self.sendMessage('%s darf hier jetzt sprechen!' % nick)

    def devoice_func(self, sender, args):
        nick = args[0]
        self.sock.devoice(nick)
        self.sendMessage('%s darf hier nicht mehr sprechen!' % nick)
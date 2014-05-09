from plugin import Plugin

class IRC(Plugin):

    def onLoad(self):
        # commands
        self.addCommand('kick', self.kick_func, 'kick <user> [<reason>] | kick <user> [with <reason>]')
        self.addCommand('cc', self.cc_func, 'cc <newchan> | part current channel and join <newchan>')
        self.addCommand('op', self.op_func, 'op <nick> | give <nick> op rights')
        self.addCommand('deop', self.deop_func, 'deop <nick> | remove <nick>s op rights')
        self.addCommand('voice', self.voice_func, 'voice <nick> | allow <nick> to speak')
        self.addCommand('devoice', self.devoice_func, 'devoice <nick> | deny <nick> to speak')

    def kick_func(self, sender, args):
        if len(args) == 1:
            self.sock.kick(args[0])
        elif len(args) > 1:
            self.sock.kick(args[0], ' '.join(args[1:]))

    def cc_func(self, sender, args):
        newchan = args[0]
        self.sendMessage('Ich gehe jetzt nach %s!' % newchan)
        self.sock.changeChannel(newchan)

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
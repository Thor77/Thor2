from plugin import Plugin

class Message(Plugin):

    def onLoad(self):
        self.color_code = str('\003')
        self.messages = {}
        # commands
        self.addCommand('addMessage', self.addMessage_func, 'addMessage <nick> <msg> | if <nick> joins the channel, he/she will get <message>')
        # events
        self.registerEvent('onUserJoin', self.onUserJoin)
        self.registerEvnet('onUserMessage', self.onUserMessage)

    def onUserJoin(self, eventobj):
        joiner = eventobj.getUser()
        if joiner in self.messages:
            self.sendMessage('Hallo %s, es wurden Nachrichten für dich hinterlassen:' % joiner)
            for sender in self.messages[joiner]:
                self.sendMessage('[{color}08{sender}{color}] => {color}07{nachricht}{color}'.format(color=self.color_code, sender=sender, nachricht=self.messages[joiner][sender]))
            del self.messages[joiner]
            print(self.messages)

    def addMessage_func(self, sender, args):
        nick = args[0]
        msg = ' '.join(args[1:])
        if nick in self.messages:
            self.messages[nick].append(sender, msg)
            print(self.messages)
        else:
            self.messages[nick] = {sender, msg} # {'nick' : {'sender1' : 'nachricht1', 'sender2' : 'nachricht2'}, ...}
            print(self.messages)
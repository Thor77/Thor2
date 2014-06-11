from plugin import Plugin

class Message(Plugin):

    def onLoad(self):
        self.color_code = str('\003')
        self.messages = {}
        # commands
        self.addCommand('addMessage', self.addMessage_func, 'addMessage <nick> <msg> | if <nick> joins the channel, he/she will get <message>')
        # events
        self.registerEvent('onUserJoin', self.onUserJoin)
        self.registerEvent('onUserMessage', self.onUserMessage)
        self.registerEvent('onUserNickChange', self.onUserNickChange)

    def onUserJoin(self, eventobj):
        joiner = eventobj.getUser()
        if joiner in self.messages:
            self.sendWaitingMessages(joiner)

    def onUserMessage(self, eventobj):
        nick = eventobj.getSender()
        if nick in self.messages:
            self.sendWaitingMessages(nick)

    def onUserNickChange(self, eventobj):
        oldnick = eventobj.getOldNick()
        newnick = eventobj.getNewNick()
        if not newnick in self.messages and not oldnick in self.messages:
            return
        if newnick.lower().find('afk') == -1 and newnick.lower().find('off') == -1:
            self.sendWaitingMessages(oldnick)
        else:
            self.messages[newnick] = self.messages[oldnick]
            del self.messages[oldnick]

    def addMessage_func(self, sender, args):
        nick = args[0]
        msg = ' '.join(args[1:])
        if nick in self.messages:
            self.messages[nick].append({sender : msg})
        else:
            self.messages[nick] = [{sender : msg}] # {'nick' : {'sender1' : 'nachricht1', 'sender2' : 'nachricht2'}, ...}
        self.sendNotice('Message successfully added!', sender)
        self.sendNotice('Message: %s' % msg, sender)
        self.sendNotice('Nick: %s' % nick, sender)

    def sendWaitingMessages(self, nick):
        self.sendMessage('Hallo %s, es wurden Nachrichten für dich hinterlassen:' % nick)
        for d in self.messages[nick]:
            for sender in d:
                msg = d[sender]
                self.sendMessage('[{color}15{sender}{color}] => {color}03{nachricht}{color}'.format(color=self.color_code, sender=sender, nachricht=msg))
        del self.messages[nick]
from plugin import Plugin

class General(Plugin):
    def onLoad(self):
        # commands
        self.addCommand('say', self.say_func, 'say <message> | send <message> to the current channel')
        self.addCommand('reload', self.reload_func, 'Reload plugins')
        self.addCommand('quit', self.quit_func, 'Disconnect from the server and exit')
        self.addCommand('setmsgdelay', self.changeMessageDelay_func, 'cdelay <seconds> | change the delay between messages sent by the bot to <seconds>')
        self.addCommand('showmsgdelay', self.showMessageDelay_func, 'shows the current message-delay')
        self.addCommand('raw', self.raw_func, 'raw <raw> | sends <raw> to the server')

        # events
        self.registerEvent('onUserMessage', self.onMessage)

    def onMessage(self, eventobj):
        #self.sendMessage('Hi %s thank you for sending me %s!' % (eventobj.getSender(), eventobj.getMessage()))
        pass

    def say_func(self, sender, args):
        msg = ' '.join(args)
        self.sendMessage(msg)

    def reload_func(self, sender, args):
        self.sendMessage('Reloading...')
        self.sock.reloadPlugins()
        self.sendMessage('Finished reloading!')

    def quit_func(self, sender, args):
        self.sock.quit('%s ist schuld!' % sender)

    def changeMessageDelay_func(self, sender, args):
        newdelay = float(args[0])
        self.messageDelay = newdelay
        self.sendNotice('Message-delay successfull changed to %s!' % newdelay, sender)

    def showMessageDelay_func(self, sender, args):
        self.sendNotice('Current message-delay: %s' % self.messageDelay, sender)

    def raw_func(self, sender, args):
        raw = ' '.join(args)
        self.sock.debug('--%s--' % sender, 2)
        self.sock._send(raw)
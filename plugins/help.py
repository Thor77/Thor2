from plugin import Plugin

class Help(Plugin):

    def onLoad(self):
        self.color_code = str('\003')
        # commands
        self.addCommand('help', self.help_func, 'help <cmdname> | show help about command <cmdname>')
        self.addCommand('commands', self.commands_func, 'show a commandlist')
        self.addCommand('info', self.info_func, 'show infos about the bot')
        self.addCommand('plugins', self.plugins_func, 'show a pluginlist')

    def help_func(self, sender, args):
        if len(args) == 0:
            # command-list
            self.sendNotice('Try "%scommands" for a commandlist!' % self.sock.call, sender)
        elif len(args) == 1:
            # help for specific commands
            cmdlist = self.sock.commands
            if args[0] in cmdlist:
                cmdhelp = cmdlist[args[0]][1]
                self.sendNotice('Help for %s: %s' % (args[0], cmdhelp), sender)
            else:
                self.sendNotice('No command with name %s!' % args[0], sender)
        else:
            self.sendNotice('Too much arguments! Try "%shelp help" to get more information about this command!' % self.sock.call, sender)

    def commands_func(self, sender, args):
        cmdlist = self.sock.commandsByPlugin
        for plugin in cmdlist:
            self.sendMessage('[%s08%s%s] => %s' % (self.color_code, plugin, self.color_code, ', '.join(cmdlist[plugin])))

    def info_func(self, sender, args):
        self.sendMessage('Creator => {color}07Thor77{color}'.format(color=self.color_code))
        self.sendMessage('Helper => {color}07Butt4cak3{color}'.format(color=self.color_code))
        self.sendMessage('Github => {color}07https://github.com/Thor77/Thor2{color}'.format(color=self.color_code))
        self.sendMessage('Commandlist => {color}07{call}commands{color}'.format(color=self.color_code, call=self.sock.call))
        self.sendMessage('Pluginlist => {color}07{call}plugins{color}'.format(color=self.color_code, call=self.sock.call))

    def plugins_func(self, sender, args):
        self.sendMessage('Loaded Plugins => {color}07{pluginlist}{color}'.format(color=self.color_code, pluginlist=', '.join(self.sock.loadedPlugins)))
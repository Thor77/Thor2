from plugin import Plugin

class Help(Plugin):

    def onLoad(self):
        self.color_code = str('\003')
        # commands
        self.addCommand('help', self.help_func, 'help <cmdname> | show help about command <cmdname>')
        self.addCommand('allcommands', self.allcommands_func, 'show ALL commands', 1)
        self.addCommand('commands', self.commands_func, 'show all commands you can use')
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

    def allcommands_func(self, sender, args):
        cmdlist = self.sock.commandsByPlugin
        for plugin in cmdlist:
            self.sendMessage('[{color}15{plugin}{color}] => {color}03{commands}{color}'.format(color=self.color_code, plugin=plugin, commands=', '.join(cmdlist[plugin])))

    def commands_func(self, sender, args):
        your_commands = {}
        nick_lvl = self.sock.getUserLevel(sender)
        for trigger in self.sock.commands:
            if self.sock.commands[trigger][3] <= nick_lvl:
                plugin = self.sock.commands[trigger][2]
                your_commands[plugin] = trigger
        for plugin in your_commands:
            self.sendNotice('[{color}15{plugin}{color}] => {color}03{commands}{color}'.format(color=self.color_code, plugin=plugin, commands=', '.join(your_commands[plugin])), sender)

    def info_func(self, sender, args):
        self.sendMessage('Creator => {color}03Thor77{color}'.format(color=self.color_code))
        self.sendMessage('Helper => {color}03Butt4cak3{color}'.format(color=self.color_code))
        self.sendMessage('Github => {color}03https://github.com/Thor77/Thor2{color}'.format(color=self.color_code))
        self.sendMessage('Commandlist => {color}03{call}commands{color}'.format(color=self.color_code, call=self.sock.call))
        self.sendMessage('Pluginlist => {color}03{call}plugins{color}'.format(color=self.color_code, call=self.sock.call))

    def plugins_func(self, sender, args):
        self.sendMessage('Loaded Plugins => {color}07{pluginlist}{color}'.format(color=self.color_code, pluginlist=', '.join(self.sock.loadedPlugins)))
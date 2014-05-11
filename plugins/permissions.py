from plugin import Plugin

class Permissions(Plugin):
    
    def onLoad(self):
        self.color_code = str('\003')
        # commands
        self.addCommand('register', self.register_func, 'add your nick to the database', 0)
        self.addCommand('changeUserLevel', self.changeLevel_func, 'changeUserLevel <nick> <newlvl> | change <nick>s userlvl to <newlvl>', 2)
        self.addCommand('listUser', self.listusers_func, 'list users in the database', 2)

    def register_func(self, sender, args):
        permissionsdict = self.sock.getPermissionsDict()
        if sender in permissionsdict:
            self.sendNotice('You are alreay registered!', sender)
            return
        self.sock.addUser(sender)
        permissiondict_new = self.sock.getPermissionsDict()
        if sender in permissiondict_new:
            self.sendMessage('%s was successfully added to the database!' % sender)
        else:
            self.sendNotice('There was an error adding you to the database!', sender)

    def changeLevel_func(self, sender, args):
        nick = args[0]
        newlvl = int(args[1])
        userdict = self.sock.getPermissionsDict()
        if nick in userdict:
            if userdict[nick] == newlvl:
                self.sendNotice('%s alreay has this level!', sender)
            else:
                self.sock.changeUserLevel(nick, newlvl)
                self.sendMessage('UserLevel of %s successfully changed to %s!' % (nick, newlvl))
        else:
            self.sendNotice('%s is not yet registered!', sender)

    def myLevel_func(self, sender, args):
        userlvl = self.sock.getUserLevel(sender)
        self.sendNotice('Your userlevel is %s!' % userlvl, sender)

    def listusers_func(self, sender, args):
        usersdict = self.sock.getPermissionsDict()
        for nick in usersdict:
            self.sendMessage('[{color}08{nick}{color}] => {lvl}'.format(color=self.color_code, nick=nick, lvl=str(usersdict[nick])))
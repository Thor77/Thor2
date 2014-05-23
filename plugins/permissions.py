from plugin import Plugin

class Permissions(Plugin):
    
    def onLoad(self):
        self.color_code = str('\003')
        # commands
        self.addCommand('changeUserLevel', self.changeLevel_func, 'changeUserLevel <nick> <newlvl> | change <nick>s userlvl to <newlvl>', 2)
        self.addCommand('listUsers', self.listusers_func, 'list users in the database', 2)
        self.addCommand('mylevel', self.myLevel_func, 'show your permissions-lvl')
        self.addCommand('deleteUser', self.deleteUser_func, 'deleteUser <nick> | remove <nick>', 2)
        self.addCommand('adduser', self.addUser_func, 'addUser <nick> | add <nick> to the database', 1)
    def addUser_func(self, sender, args):
        nick = args[0]
        permissionsdict = self.sock.getPermissionsDict()
        if nick in permissionsdict:
            self.sendNotice('%s is alreay registered!' % nick, sender)
            return
        self.sock.addUser(nick.lower())
        permissiondict_new = self.sock.getPermissionsDict()
        if nick in permissiondict_new:
            self.sendMessage('%s was successfully added to the database!' % sender)
        else:
            self.sendNotice('There was an error adding you to the database!', sender)

    def changeLevel_func(self, sender, args):
        nick = args[0].lower()
        newlvl = int(args[1])
        userdict = self.sock.getPermissionsDict()
        if nick in userdict:
            if userdict[nick] == newlvl:
                self.sendNotice('%s alreay has this level!', sender)
            else:
                self.sock.changeUserLevel(nick, newlvl)
                self.sendMessage('UserLevel of %s successfully changed to %s!' % (nick, newlvl))
        else:
            self.sendNotice('%s is not in the database!' % nick, sender)

    def myLevel_func(self, sender, args):
        userlvl = self.sock.getUserLevel(sender.lower())
        self.sendNotice('Your userlevel is %s!' % userlvl, sender)

    def listusers_func(self, sender, args):
        usersdict = self.sock.getPermissionsDict()
        userlist = []
        for nick in usersdict:
            userlist.append('{color}15{nick}{color} [{color}03{lvl}{color}]'.format(color=self.color_code, nick=nick, lvl=str(usersdict[nick])))
        self.sendNotice(', '.join(userlist), sender)

    def deleteUser_func(self, sender, args):
        nick = args[0]
        usersdict = self.sock.getPermissionsDict()
        if nick in usersdict:
            self.sock.deleteUser(nick.lower())
            self.sendMessage('Successfully removed %s from the database!' % nick)
        else:
            self.sendNotice('%s is not in the database!' % nick, sender)
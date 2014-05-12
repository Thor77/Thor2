from plugin import Plugin

class Poll(Plugin):

    def onLoad(self):
        self.poll         = {} # { optionindex : [ option, votes, [voters] ] }
        self.poll_created = False
        self.poll_started = False
        self.poll_creator = ''
        # commands
        self.addCommand('poll', self.createPoll, 'poll <question> | creates poll with <question>')
        self.addCommand('addoption', self.addOption, 'addoption <option> | adds <option> to the active poll')
        self.addCommand('showpoll', self.showPoll, 'show the active poll')
        self.addCommand('vote', self.vote, 'vote <optionnumber> | votes for <optionnumber>')
        self.addCommand('endpoll', self.endPoll, 'ends the poll and show the result')

    def createPoll(self, sender, args):
        if self.poll_started:
            self.sendNotice('Theres already an active poll, type %sshowpoll to see it!' % self.sock.getCall() ,sender)
            return
        question = ' '.join(args)
        self.poll['question'] = [question, []]
        self.sendNotice('Created poll "%s"!' % question, sender)
        self.poll_created = True
        self.poll_creator = sender

    def addOption(self, sender, args):
        if not self.poll_created:
            self.sendNotice('No active poll! Create poll first! Try "%shelp poll"' % self.sock.getCall(), sender)
            return
        elif sender != self.poll_creator:
            self.sendNotice('You cant edit %ss poll!' % self.poll_creator, sender)
            return
        elif not self.poll_started:
            self.poll_started = True
        option = ' '.join(args)
        length = len(self.poll)
        self.poll[str(length)] = [option, 0, []]
        self.sendNotice('Added option "%s" with index %s!' % (option, length), sender)

    def showPoll(self, sender, args):
        if not self.poll_started:
            self.sendNotice('No active poll! Create poll first! Try "%shelp poll"' % self.sock.getCall(), sender)
            return
        self.sendMessage('Question: ' + self.poll['question'][0])
        print(self.poll)
        for key in self.poll:
            if key != 'question':
                index = key
                option = self.poll[key][0]
                votes = self.poll[key][1]
                self.sendMessage('%s. | %s | Votes: %s' % (index, option, votes))

    def vote(self, sender, args):
        if not self.poll_started:
            self.sendNotice('No active poll! Create poll first! Try "%shelp poll"' % self.sock.getCall(), sender)
            return
        number = args[0]
        if number in self.poll:
            if sender not in self.poll['question'][1]:
                (self.poll[number])[1] += 1
                self.sendNotice('Successfully voted for "%s"' % (self.poll[number])[0], sender)
                self.poll['question'][1].append(sender)
                self.poll[number][2].append(sender)
            else:
                self.sendNotice('You already voted!', sender)
        else:
            self.sendNotice('Invalid optionnumber! Try "%sshowpoll" for a list of options!' % self.sock.getCall(), sender)

    def endPoll(self, sender, args):
        if not self.poll_started:
            self.sendNotice('No active poll! Create poll first! Try "%shelp poll"' % self.sock.getCall(), sender)
            return
        heighest = [0, '']
        votes = 0
        for key in self.poll:
            if key != 'question':
                value = self.poll[key][1]
                votes += value
                if value > heighest[0]:
                    heighest[0] = value
                    heighest[1] = key
        heighest_key = heighest[1]
        self.sendMessage('Poll "%s" closed!' % self.poll['question'][0])
        self.sendMessage('"%s" got most votes (%s)!' % (self.poll[heighest_key][0], self.poll[heighest_key][1]))

        # reset poll
        self.poll = {}
        self.poll_started = False
        self.poll_created = False
        self.poll_creator = ''
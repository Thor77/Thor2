from plugin import Plugin
try:
    import requests
    requests_available = True
except ImportError:
    requests_available = False

class Steam(Plugin):
    def onLoad(self):
        self.color_code = str('\003')
        # commands
        if requests_available:
            self.addCommand('steamplayers', self.steamPlayers_func, 'shows count of currently online players on steam')
            self.addCommand('steamstatus', self.steamStatus_func, 'shows the status of steam services')
            self.addCommand('dotamm', self.dotaPlayer_func, 'shows the count of players currently in Dota 2 Matchmaking')
            self.addCommand('dotammtime', self.dotaMMTime_func, 'shows the average waiting time in the Dota 2 Matchmaking')
            self.addCommand('steamall', self.steamAll_func, 'shows all informations about steam')

    def steamPlayers_func(self, sender, args):
        r = requests.get('http://steamstat.us/status.json').json()
        online_count = r['services']['online']['title']
        self.sendMessage('There are currently {color}07{count}{color} players online on Steam!'.format(color=self.color_code, count=online_count))

    def steamStatus_func(self, sender, args):
        r = requests.get('http://issteamdown.com/status.json').json()
        statuses = r['statuses']
        for service in statuses:
            title = service['title']
            s = service['status']
            if s:
                service_status = self.color_code + '03Online' + self.color_code
            else:
                service_status = self.color_code + '04Offline' + self.color_code
            self.sendMessage('%s is %s' % (title, service_status))

    def dotaPlayer_func(self, sender, args):
        r = requests.get('http://steamstat.us/status.json').json()
        curr_searching = r['services']['dota_mm_searching']['title']
        self.sendMessage('There are currently {color}07{count}{color} players in the Dota 2 Matchmaking!'.format(color=self.color_code, count=curr_searching))

    def dotaMMTime_func(self, sender, args):
        r = requests.get('http://steamstat.us/status.json').json()
        average_waittime = r['services']['dota_mm_average']['title']
        self.sendMessage('Average waittime in the Dota 2 Matchmaking: {color}07{count}{color}!'.format(color=self.color_code, count=average_waittime))

    def steamAll_func(self, sender, args):
        # players online
        r = requests.get('http://steamstat.us/status.json').json()
        online_count = r['services']['online']['title']

        # services
        r = requests.get('http://issteamdown.com/status.json').json()
        statuses = r['statuses']
        statuses_dict = []
        for service in statuses:
            title = service['title']
            s = service['status']
            if s:
                service_status = self.color_code + '03Online' + self.color_code
            else:
                service_status = self.color_code + '04Offline' + self.color_code
            statuses_dict.append('%s: %s07%s%s' % (title, self.color_code, service_status, self.color_code))


        # dota mm players
        r = requests.get('http://steamstat.us/status.json').json()
        curr_searching = r['services']['dota_mm_searching']['title']

        # dota mm time
        r = requests.get('http://steamstat.us/status.json').json()
        average_waittime = r['services']['dota_mm_average']['title']

        #
        self.sendMessage('Current Steam Stats')
        self.sendMessage('powered by steamstat.us and issteamdown.com')
        for msg in statuses_dict:
            self.sendMessage(msg)
        self.sendMessage('Players online: %s07%s%s' % (self.color_code, online_count, self.color_code))
        self.sendMessage('Players in Dota 2 Matchmaking: %s07%s%s' % (self.color_code, curr_searching, self.color_code))
        self.sendMessage('Average waiting Time in Dota 2 Matchmaking: %s07%s%s' % (self.color_code, average_waittime, self.color_code))
from plugin import Plugin
import requests

class OpenWeatherMap(Plugin):

    def onLoad(self):
        self.addCommand('weather'. self.weather_cmd, 'weather <city> | show weather for <city>')

    def getWeather(self, location):
        owm_url = 'http://api.openweathermap.org/data/2.5/weather'

        r = requests.get(owm_url + '?q=%s' % location).json()
        cod = int(r['cod'])
        if cod != 200:
            return None
        city = r['name']
        country = r['sys']['country']
        main = r['weather'][0]['main']
        description = r['weather'][0]['description']
        temperature = round(int(r['main']['temp']) - 273.15, 2)
        return (city, country, main, description, temperature)


    def weather_cmd(self, sender, args):
        location = args[0]
        weather = self.getWeather(location)
        if weather == None:
            self.sendNotice('Can\'t find this location!', sender)
        else:
            city, country, main, description, temperature = weather
            self.sendMessage('Weather in {city}, {country}: {temperature} and {main} ({description})'.format(city=city, country=country, temperature=temperature, main=main, description=description))
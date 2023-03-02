import requests

from manager.tts_manager import speak

weather_api = "a26a13556f93a14df0a58e1fd6328495"


class WeatherManager:
    def ask_weather(self, keyword):
        if "domani" in keyword.lower():
            print("Tomorrow")
            keyword.replace('domani a ', '').strip()
            url = f"http://api.weatherstack.com/forecast?access_key={weather_api}&query={keyword}"
        else:
            print("Today")
            url = f"http://api.weatherstack.com/current?access_key={weather_api}&query={keyword}"

        response = requests.get(url)
        data = response.json()
        if 'current' in data:
            temperature = data['current']['temperature']
            weather_description = data['current']['weather_descriptions'][0]
            if "domani" in keyword.lower():
                keyword.replace('domani a ', '').strip()
                speak(f"Temperatura a {keyword} per domani: {temperature} gradi Celsius con le seguenti condizioni: "
                      + weather_description)
            else:
                speak(f"Temperatura attuale a {keyword}: {temperature} gradi Celsius con le seguenti condizioni: "
                      + weather_description)
        else:
            speak(f"Impossibile ottenere le informazioni meteorologiche per {keyword}")


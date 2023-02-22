import requests

from tts_manager import speak

weather_api = "a26a13556f93a14df0a58e1fd6328495"


class WeatherManager:
    def ask_weather(self, keyword):
        url = f"http://api.weatherstack.com/current?access_key={weather_api}&query={keyword}"
        response = requests.get(url)
        data = response.json()
        if 'current' in data:
            temperature = data['current']['temperature']
            weather_description = data['current']['weather_descriptions'][0]
            # description_translated = translation(weather_description)
            # BUG poiche weather_description è in inglese, non trovo API gratuite
            speak(f"Temperatura attuale a {keyword}: {temperature} gradi Celsius con le seguenti condizioni: "
                  + weather_description)
        else:
            speak(f"Impossibile ottenere le informazioni meteorologiche per {keyword}")

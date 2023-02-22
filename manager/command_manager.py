import re

from manager.gpt_manager import GptManager
from manager.tts_manager import speak
from manager.weather_manager import WeatherManager
from manager.yt_manager import YtManager


class CommandManager:
    def __init__(self):
        self.yt_manager = YtManager()
        self.weather_manager = WeatherManager()
        self.gpt_manager = GptManager()
        self.cmds = {
            "play_yt_cmds": [r"puoi riprodurre (.*)", r"puoi suonare (.*)", r"metti (.*) ", r"riproduci (.*)"],
            "download_yt_cmds": [r"download (.*)", r"puoi scaricare (.*)"],
            "emilio_cmds": [r"mortimer", r"bellibus"],
            "weather_cmds": [r"puoi dirmi il meteo di (.*)", r"puoi dirmi il meteo a (.*)", r"dimmi il meteo a (.*)",
                             r"puoi dirmi il meteo attuale di (.*)", r"meteo  di (.*)", r"meteo (.*)", r"meteo a (.*)"]
        }

    def manage(self, keyword):
        for group in self.cmds:
            for command in self.cmds[group]:
                match = re.search(command, keyword)
                if match:
                    arg = match.group(1)
                    print("Pattern trovato!")
                    if group == "play_yt_cmds":
                        self.yt_manager.play_yt(arg)
                    elif group == "download_yt_cmds":
                        self.yt_manager.download_yt(arg)
                    elif group == "emilio_cmds":
                        speak(arg)
                    elif group == "weather_cmds":
                        self.weather_manager.ask_weather(arg)
                    return

        print("Pattern non trovato!")
        self.gpt_manager.ask(keyword)

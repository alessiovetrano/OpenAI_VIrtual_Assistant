import re

from manager.gpt_manager import GptManager
from manager.tts_manager import speak
from manager.weather_manager import WeatherManager
from manager.yt_manager import YtManager
from manager.time_manager import TimeManager
from manager.todolist_manager import ToDoListManager


class CommandManager:
    def __init__(self):
        self.yt_manager = YtManager()
        self.weather_manager = WeatherManager()
        self.gpt_manager = GptManager()
        self.time_manager = TimeManager()
        self.todo_manager = ToDoListManager()
        self.cmds = {
            "play_yt_cmds": [r"puoi riprodurre (.*)", r"puoi suonare (.*)", r"metti (.*) ", r"riproduci (.*)"],
            "download_yt_cmds": [r"download (.*)", r"puoi scaricare (.*)", r"scarica (.*)", r"aggiungi"],
            "emilio_cmds": [r"mortimer", r"bellibus"],
            "weather_cmds": [r"puoi dirmi il meteo di (.*)", r"puoi dirmi il meteo a (.*)", r"dimmi il meteo a (.*)",
                             r"puoi dirmi il meteo attuale di (.*)", r"meteo  di (.*)", r"meteo (.*)", r"meteo a (.*)"],
            "manager_audio": [r"stoppa", r"play", r"prossima", r"precedente"],
            "ask_time": [r"che ore sono?", r"che ora è?", r"puoi dirmi l'ora?", "dimmi l'ora", "puoi dirmi l'orario"],
            "ask_date": [r"che giorno è oggi?", r"che giorno è?", r"puoi dirmi la data di oggi",
                         r"dimmi la data di oggi"],
            "add_task": [r"aggiungi (.*) alle cose da fare", r"aggiungi alla lista \"(.*)\"",
                         r"aggiungi (.*) alla mia lista delle cose da fare \"(.*)\"",
                         r"aggiungi (.*) alla lista delle cose da fare",
                         r"aggiungi \"(.*)\" alla mia lista delle cose da fare"],
            "remove_task": ["rimuovi (.*) dalla lista delle cose da fare", "rimuovi (.*) delle cose da fare",
                            "elimina il task (.*)"],
            "get_task_list": [r"puoi dirmi le cose da fare", r"puoi dirmi le cose che devo fare",
                              r"puoi dirmi la lista dele cose da fare"]
        }

    def manage(self, keyword):
        for group in self.cmds:
            for command in self.cmds[group]:
                match = re.search(command, keyword)
                if match:
                    if len(match.groups()) == 1:
                        arg = match.group(1)
                    else:
                        arg = match.string
                    print("Pattern trovato!")
                    if group == "play_yt_cmds":
                        self.yt_manager.play_yt(arg)
                    elif group == "download_yt_cmds":
                        self.yt_manager.download_yt(arg)
                    elif group == "emilio_cmds":
                        speak(arg)
                    elif group == "weather_cmds":
                        self.weather_manager.ask_weather(arg),
                    elif group == "manager_audio":
                        print(arg)
                        self.yt_manager.manager_audio(arg)
                    elif group == "ask_time":
                        self.time_manager.ask_time()
                    elif group == "ask_date":
                        self.time_manager.ask_date()
                    elif group == "add_task":
                        self.todo_manager.add_task(arg)
                    elif group == "remove_task":
                        self.todo_manager.remove_task(arg)
                    elif group == "get_task_list":
                        self.todo_manager.get_task_list()
                    return

        print("Pattern non trovato!")
        self.gpt_manager.ask(keyword)

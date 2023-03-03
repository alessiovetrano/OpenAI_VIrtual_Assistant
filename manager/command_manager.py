import re

from manager import time_manager
from manager.gpt_manager import GptManager
from manager.tts_manager import speak
from manager.weather_manager import WeatherManager
from manager.yt_manager import YtManager
from manager.todolist_manager import ToDoListManager
from manager.news_manager import NewsManager
from manager.live_football_manager import LiveFootball
from manager.mail_manger import MailManager
from manager.shipment_manager import ShipmentManager
from manager.waze_manager import WazeManager


class CommandManager:
    def __init__(self):
        self.yt_manager = YtManager()
        self.weather_manager = WeatherManager()
        self.gpt_manager = GptManager()
        self.todo_manager = ToDoListManager()
        self.news_manager = NewsManager()
        self.live_football = LiveFootball()
        self.mail_manager = MailManager(self.gpt_manager)
        self.ship_manager = ShipmentManager()
        self.waze_manager = WazeManager()
        self.cmds = {
            "play_yt_cmds": [r"puoi riprodurre (.*)", r"puoi suonare (.*)", r"metti (.*) ", r"riproduci (.*)"],
            "download_yt_cmds": [r"download (.*)", r"puoi scaricare (.*)", r"scarica (.*)", r"aggiungi"],
            "emilio_cmds": [r"mortimer", r"bellibus"],
            "weather_cmds": [r"puoi dirmi il meteo di (.*)", r"puoi dirmi il meteo a (.*)", r"dimmi il meteo a (.*)",
                             r"puoi dirmi il meteo attuale di (.*)", r"meteo  di (.*)", r"meteo (.*)", r"meteo a (.*)"], #TESTARE IN PIU OCCASIONI MA GESTITO IL METEO ANCHE PER IL GIORNO SEGUENTE
            "manager_audio": [r"stoppa", r"play", r"prossima", r"precedente"], #GESTIRE BENE I PATTERN PER ANDARE AVANTI E INDIETRO NELLE PLAYLIST
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
                              r"puoi dirmi la lista delLe cose da fare"],
            "ask_news": [r"dimmi le notizie",r"dimmi le notizie di oggi",r"cosa è successo oggi",r"dimmi cosa è successo oggi"], #DA RIVEDERE LO SPEAKING
            "get_match": [r"dimmi cosa sta facendo il (.*)", r"dimmi cosa sta facendo la (.*)",r"cosa sta facendo la (.*)",r"cosa sta facendo il (.*)"],
            "send_email": [r"manda un'email"], #DA RIVEDERE
            "get_carrier": [r"traccia pacco"], #DA RIVEDERE,
            "get_traffico_info" : [r"traffico"] #PATTERN DA RIVEDERE
            #RIVEDERE GLI SPEAKING
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
                        speak('mooortiiiiimer')
                    elif group == "weather_cmds":
                        self.weather_manager.ask_weather(arg),
                    elif group == "manager_audio":
                        self.yt_manager.manager_audio(arg)
                    elif group == "ask_time":
                        time_manager.ask_time()
                    elif group == "ask_date":
                        time_manager.ask_date()
                    elif group == "add_task":
                        self.todo_manager.add_task(arg)
                    elif group == "remove_task":
                        self.todo_manager.remove_task(arg)
                    elif group == "get_task_list":
                        self.todo_manager.get_task_list()
                    elif group == "ask_news":
                        self.news_manager.ask_news()
                    elif group == "get_match":
                        self.live_football.get_match(arg)
                    elif group == "send_email":
                        self.mail_manager.send_email(keyword)
                    elif group == "get_carrier":
                        self.ship_manager.get_carrier()
                    elif group == "get_traffico_info":
                        self.waze_manager.get_traffico_info()
                    return

        print("Pattern non trovato!")
        response = self.gpt_manager.ask(keyword)
        print("Risposta: " + response)
        speak(response)

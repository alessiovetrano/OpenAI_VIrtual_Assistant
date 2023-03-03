import re
import os
from manager.tts_manager import speak

class TravelManager:
    def __init__(self, gpt_manager):
        self.gpt_manager = gpt_manager

    def ask_travel(self,data):
        answer = str(self.gpt_manager.ask(data))
        answer = "\n".join(line.strip() for line in answer.splitlines() if line.strip())
        file_name = "viaggio.txt"
        if not os.path.exists(file_name):
            open(file_name, 'w').close()
        with open(file_name, 'w') as f:
            f.write(answer)
        name = str(self.gpt_manager.ask("dammi come risposta solo un nome per il file che contiene queste informazioni in formato txt, esempio: 'nome.txt'"))
        print(file_name, name)
        os.rename(file_name, name)
        self.gpt_manager.clear_history(2)


    def get_travel_info(self,destination):
        destination_formatted = destination.title()  # Converte la prima lettera in maiuscolo e il resto in minuscolo
        matching_files = [f for f in os.listdir() if os.path.isfile(f) and destination_formatted in f]
        if not matching_files:
            speak(f"Non ci sono informazioni di viaggio disponibili per {destination}.")
        else:
            file_name = matching_files[0]
            with open(file_name, 'r') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
                for line in lines:
                    speak(line)
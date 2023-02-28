from datetime import datetime
from manager.tts_manager import speak

class TimeManager:

    def __init__(self):
        self.current_time = datetime.now()

    def ask_time(self):
        self.current_time = datetime.now()
        speak(self.current_time.strftime("L'ora è " + "%H:%M:%S"))
    def ask_date(self):
        self.current_time = datetime.now()
        speak("Oggi è il giorno: " + self.current_time.strftime("%Y-%m-%d"))

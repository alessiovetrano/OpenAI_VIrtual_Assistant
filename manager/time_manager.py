import locale
import os
from datetime import datetime
from manager.tts_manager import speak


def ask_time():
    current_time = datetime.now()
    speak("Sono le ore " + current_time.strftime("%H:%M"))


def ask_date():
    current_time = datetime.now()
    locale.setlocale(locale.LC_ALL, locale.getlocale())
    speak("Oggi è " + current_time.strftime("%A %-d %B %Y"))

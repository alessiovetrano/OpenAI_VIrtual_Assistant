import datetime
import time
import threading

from pygame.time import set_timer

from manager.tts_manager import speak


class AlarmManager:

    def set_alarm(self, alarm_time):
        alarm_hour, alarm_minute = map(int, alarm_time.split(":"))
        while True:
            now = datetime.datetime.now()
            current_hour, current_minute = now.hour, now.minute
            if current_hour == alarm_hour and current_minute == alarm_minute:
                speak("SVEGLIA -- LUCA PAR O CAZZZZ")
                break
            time.sleep(60)

    def run_alarm(self, alarm_time):
        alarm_thread = threading.Thread(target=self.set_alarm, args=(alarm_time,))
        alarm_thread.start()

    def set_timer(self,duration):
        end_time = datetime.datetime.now() + datetime.timedelta(minutes=duration)
        while datetime.datetime.now() < end_time:
            remaining_time = end_time - datetime.datetime.now()
            print("Tempo rimanente: ", remaining_time.seconds, " secondi")
            time.sleep(1)
        print("Timer finito")
        speak("TIMER CONCLUSO") #METTERE UN MP3 CON SQUILLO DA RIPRODURRE

    def run_timer(self,duration):
        timer_thread = threading.Thread(target=self.set_timer, args=(duration,))
        timer_thread.start()
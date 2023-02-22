import speech_recognition as sr

import log_manager


class SpeechToTextManager:
    def __init__(self):
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        with self.m as source:
            self.r.adjust_for_ambient_noise(source, duration=3.5)
            self.r.dynamic_energy_threshold = True

    def listen(self):
        print("In ascolto...")
        with self.m as source:
            audio = self.r.listen(source)
        print("Elaborazione in corso...")
        old_stdout = log_manager.hide_logs(1)
        value = None
        try:
            value = self.r.recognize_google(audio, language='it-IT', show_all=False).lower()
        except sr.UnknownValueError:
            print("Segnale non catturato")
        except sr.RequestError as e:
            print("{0}".format(e))
        finally:
            log_manager.show_logs(old_stdout, 1)
            if value is not None:
                if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                    print(u"Hai detto: {}".format(value).encode("utf-8"))
                else:  # this version of Python uses unicode for strings (Python 3+)
                    print("Hai detto: {}".format(value))
            return value

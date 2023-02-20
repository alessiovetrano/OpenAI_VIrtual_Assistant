import openai
import speech_recognition as sr
import pyttsx3

openai.api_key = "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"

def ask():
    response = openai.Completion.create(
        engine="davinci",
        prompt=value,
        temperature=0.5,
        max_tokens=500
    )
    # Stampa il testo generato
    print(response.choices[0].text)
    Speak(response.choices[0].text)


def Speak(audio):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[36].id)  # index 36 per l'ITALIANO
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    engine.say(audio)
    engine.runAndWait()


if __name__ == '__main__':

    r = sr.Recognizer()
    m = sr.Microphone()
    value = None
    try:
        while True:
            with m as source:
                r.adjust_for_ambient_noise(source, duration=3)
                r.dynamic_energy_threshold = True
            print("Set minimum energy threshold to {}".format(r.energy_threshold))
            print("Prova a parlare")
            with m as source:
                audio = r.listen(source)
            print("SEGNALE CATTURATO, elaborazione...")
            try:
                value = r.recognize_google(audio, language='it-IT')
                if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                    print(u"Hai detto {}".format(value).encode("utf-8"))
                else:  # this version of Python uses unicode for strings (Python 3+)
                    print("Hai detto {}".format(value))
            except sr.UnknownValueError:
                print("Segnale non catturato")
            except sr.RequestError as e:
                print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
            ask()
    except KeyboardInterrupt:
        pass

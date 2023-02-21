import os
import openai
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound


# setto lingaggio per sintetizzatore
language = "it"
#setting openai
openai.api_key = "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"
model_engine = "text-davinci-003"
temperature = 0.5

def ask():
    response = openai.Completion.create(
        engine=model_engine,
        prompt=value,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=temperature,
    )
    print("Risposta: " + response.choices[0].text.strip())
    Speak(response.choices[0].text)


def Speak(text):
    tts = gTTS(text=text, lang=language)
    tts.save("answer_OPENAI.mp3")
    # utilizzo di vlc per la riproduzione utilizzando sintetizzatore di google
    os.system("cvlc answer_OPENAI.mp3")
    #playsound('answer_OPENAI.mp3', True)
if __name__ == '__main__':

    r = sr.Recognizer()
    m = sr.Microphone()
    value = None
    try:
        while True:
            with m as source:
                r.adjust_for_ambient_noise(source, duration=3.5)
                r.dynamic_energy_threshold = True
            print("Set minimum energy threshold to {}".format(r.energy_threshold))
            print("Ora rova a parlare...")
            with m as source:
                audio = r.listen(source)
            print("Segnale catturato con successo, elaborazione in corso...")
            try:
                value = r.recognize_google(audio, language='it-IT')
                if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                    print(u"Hai detto {}".format(value).encode("utf-8"))
                else:  # this version of Python uses unicode for strings (Python 3+)
                    print("Hai detto {}".format(value))
            except sr.UnknownValueError:
                print("Segnale non catturato")
            except sr.RequestError as e:
                print("{0}".format(e))
            ask()
    except KeyboardInterrupt:
        pass

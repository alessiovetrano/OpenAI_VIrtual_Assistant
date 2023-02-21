import json
import os
import sys

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
old_prompts = []

def ask(value):
    # Aggiunge la richiesta alla conversazione
    old_prompts.append(value)
    text = ""
    for prompt in old_prompts:
        text += prompt + "\n"

    response = openai.Completion.create(
        engine=model_engine,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=temperature,
        prompt=text
    )

    respText = response["choices"][0]["text"].strip()
    # Aggiunge la risposta alla conversazione
    old_prompts.append(respText)

    # Elimina i primi output per evitare di riempire la memoria
    if len(old_prompts) >= 1000:
        old_prompts.pop(0)

    print("Risposta: " + respText)
    Speak(respText)

def Speak(text):
    tts = gTTS(text=text, lang=language)
    tts.save("answer_OPENAI.mp3")
    # utilizzo di vlc per la riproduzione utilizzando sintetizzatore di google
    os.system("cvlc --play-and-exit answer_OPENAI.mp3")
    #playsound('answer_OPENAI.mp3', True)

def hideErrors():
    devnull = os.open(os.devnull, os.O_WRONLY)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)

if __name__ == '__main__':
    hideErrors()
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
                ask(value)
            except sr.UnknownValueError:
                print("Segnale non catturato")
            except sr.RequestError as e:
                print("{0}".format(e))
    except KeyboardInterrupt:
        pass
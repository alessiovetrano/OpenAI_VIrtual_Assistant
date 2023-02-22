# define PY_SSIZE_T_CLEAN
import requests
from googletrans import Translator

from youtube_search import YoutubeSearch
import os
import sys
import re
import openai
import speech_recognition as sr
from gtts import gTTS
import pytube
from pydub import AudioSegment

# setto lingaggio per sintetizzatore
language = "it"
# setting openai
openai.api_key = "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"
model_engine = "text-davinci-003"
temperature = 0.5
old_prompts = []
#weather
weather_api = "a26a13556f93a14df0a58e1fd6328495"
translator = Translator()

def translation(text):
    return translator.translate(text, dest='it').text

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


def ask_weather(keyword):
    url = f"http://api.weatherstack.com/current?access_key={weather_api}&query={keyword}"
    response = requests.get(url)
    data = response.json()
    if 'current' in data:
        temperature = data['current']['temperature']
        weather_description = data['current']['weather_descriptions'][0]
        #description_translated = translation(weather_description)
        #BUG poiche weather_description è in inglese, non trovo API gratuite
        Speak(f"Temperatura attuale a {keyword}: {temperature} gradi Celsius con le seguenti condizioni: " + weather_description)
    else:
        Speak(f"Impossibile ottenere le informazioni meteorologiche per {keyword}")




def play_yt(keyword):
    Speak("Certo, riproduco: " + keyword)
    search_word = keyword
    results = YoutubeSearch(search_word, max_results=1).to_dict()
    if len(results) > 0:
        video_link = "https://www.youtube.com/watch?v=" + results[0]['id']
        yt = pytube.YouTube(video_link)
        video_file = yt.streams.get_highest_resolution().download()
        audio_file = AudioSegment.from_file(video_file, format="mp4")
        audio_file.export("tmp_audio.mp3", format="mp3")
        os.system("cvlc --play-and-exit tmp_audio.mp3")
        os.remove("tmp_audio.mp3")
        #rimuovere file mp4
    else:
        print("Nessun video trovato per la ricerca:", search_word)


def download_yt(keyword):
    Speak("Certo, scarico: " + keyword)
    search_word = keyword
    results = YoutubeSearch(search_word, max_results=1).to_dict()
    if len(results) > 0:
        #AGGIUNGERE PATH CARTELLA PER PLAYLIST
        video_link = "https://www.youtube.com/watch?v=" + results[0]['id']
        yt = pytube.YouTube(video_link)
        video_file = yt.streams.get_highest_resolution().download()
        audio_file = AudioSegment.from_file(video_file, format="mp4")
        audio_file.export(video_file, format="mp3")
    else:
        print("Nessun video trovato per la ricerca:", search_word)


def diz_emilio(value):
    Speak(value)


pattern_functions = {
    r"puoi riprodurre (.*)": play_yt,
    r"puoi suonare (.*)": play_yt,
    r"metti (.*) ": play_yt,
    r"riproduci (.*)": play_yt,
    r"download (.*)": download_yt,
    r"puoi scaricare (.*)": download_yt,
    r"mortimer": diz_emilio,
    r"bellibus": diz_emilio,
    r"puoi dirmi il meteo di (.*)": ask_weather,
    r"puoi dirmi il meteo a (.*)": ask_weather,
    r"dimmi il meteo a (.*)": ask_weather,
    r"puoi dirmi il meteo attuale di (.*)": ask_weather,
    r"meteo  di (.*)": ask_weather,
    r"meteo (.*)": ask_weather,
    r"meteo a (.*)": ask_weather
}


def ask_custom_questions(value):
    # espressione regolare per capire pattern
    # cerca un match in ogni pattern
    for pattern, func in pattern_functions.items():
        match = re.search(pattern, value)
        if match:
            print("Pattern trovato")
            if func == diz_emilio:
                func(value)
            elif func in [play_yt, download_yt, ask_weather]:
                arg = match.group(1)
                func(arg)
            return
    # Nessun pattern trovato
    print("Pattern non trovato")
    ask(value)



def Speak(text):
    tts = gTTS(text=text, lang=language)
    tts.save("answer_OPENAI.mp3")
    os.system("cvlc --play-and-exit answer_OPENAI.mp3")


def hideLogs(fd=2):
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_std = os.dup(fd)
    sys.stderr.flush()
    os.dup2(devnull, fd)
    os.close(devnull)
    return old_std


def showLogs(old_std, fd=2):
    os.dup2(old_std, fd)
    os.close(old_std)


if __name__ == '__main__':
    #hideLogs()
    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source:
        r.adjust_for_ambient_noise(source, duration=3.5)
        r.dynamic_energy_threshold = True
    try:
        while True:
            print("In ascolto...")
            with m as source:
                audio = r.listen(source)
            print("Elaborazione in corso...")
            old_stdout = hideLogs(1)
            try:
                value = r.recognize_google(audio, language='it-IT', show_all=False).lower()
                showLogs(old_stdout, 1)
                if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                    print(u"Hai detto: {}".format(value).encode("utf-8"))
                else:  # this version of Python uses unicode for strings (Python 3+)
                    print("Hai detto: {}".format(value))
                ask_custom_questions(value)
            except sr.UnknownValueError:
                print("Segnale non catturato")
            except sr.RequestError as e:
                print("{0}".format(e))
            finally:
                showLogs(old_stdout, 1)
    except KeyboardInterrupt:
        pass

import re
import threading
import time
from io import BytesIO

from pygame import mixer
from gtts import gTTS

language = "it"
streams = []


def load_phrase(index, phrase):
    tts = gTTS(text=phrase, lang=language)
    streams[index] = BytesIO()
    tts.write_to_fp(streams[index])
    streams[index].seek(0)


def speak(text):
    if len(text) > 50:
        phrases = split_text(text)
    else:
        phrases = [text]

    threads = []
    streams.clear()
    for i in range(len(phrases)):
        streams.append(None)
        threads.append(threading.Thread(target=load_phrase, args=(i, phrases[i].strip(),)))
        threads[i].start()

    mixer.init()
    for i in range(len(phrases)):
        threads[i].join()
        mixer.music.load(streams[i], "mp3")
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(0.3)


def split_text(text):
    return re.split(r'\.|;|:|!|\?', text)

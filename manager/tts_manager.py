import re
import threading
import time
from io import BytesIO

import pygame
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
        phrase = phrases[i].strip()
        if len(phrase) > 0:
            streams.append(None)
            threads.append(threading.Thread(target=load_phrase, args=(i, phrases[i].strip(),)))
            threads[i].start()

    pygame.mixer.init()
    for i in range(len(streams)):
        threads[i].join()
        audio = pygame.mixer.Sound(streams[i])
        audio.play()
        time.sleep(audio.get_length())
    pygame.mixer.quit()


def split_text(text):
    return re.split(r'\.|;|:|!|\?', text)

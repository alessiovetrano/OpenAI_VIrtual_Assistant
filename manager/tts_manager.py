import re
import threading
import time

import vlc
from gtts import gTTS

language = "it"


def load_phrase(index, phrase):
    tts = gTTS(text=phrase, lang=language)
    tts.save("answers/answer" + str(index) + ".mp3")


def speak(text):
    if len(text) > 50:
        phrases = split_text(text)
    else:
        phrases = [text]

    threads = []
    for i in range(len(phrases)):
        threads.append(threading.Thread(target=load_phrase, args=(i, phrases[i].strip(),)))
        threads[i].start()

    for i in range(len(phrases)):
        threads[i].join()
        instance = vlc.Instance()
        player = instance.media_player_new()
        media = instance.media_new("answers/answer" + str(i) + ".mp3")
        media.get_mrl()
        player.set_media(media)
        player.play()
        time.sleep(0.5)
        duration = player.get_length() / 1000
        time.sleep(duration)


def split_text(text):
    return re.split(r'\.|;|:|!|\?', text)

import os

import vlc
from gtts import gTTS

language = "it"


def speak(text):
    tts = gTTS(text=text, lang=language)
    tts.save("answer_OPENAI.mp3")
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new("answer_OPENAI.mp3")
    media.get_mrl()
    player.set_media(media)
    player.play()

import os

from gtts import gTTS

language = "it"


def speak(text):
    tts = gTTS(text=text, lang=language)
    tts.save("answer_OPENAI.mp3")
    os.system("cvlc --play-and-exit answer_OPENAI.mp3")

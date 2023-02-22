import os

import pytube
from pydub import AudioSegment
from youtube_search import YoutubeSearch

from manager.tts_manager import speak


class YtManager:
    def play_yt(self, keyword):
        speak("Certo, riproduco: " + keyword)
        search_word = keyword
        results = YoutubeSearch(search_word, max_results=1).to_dict()
        if len(results) > 0:
            video_link = "https://www.youtube.com/watch?v=" + results[0]['id']
            yt = pytube.YouTube(video_link)
            video_file = yt.streams.get_highest_resolution().download()
            audio_file = AudioSegment.from_file(video_file, format="mp4")
            audio_file.export("tmp_audio.mp3", format="mp3")
            os.system("cvlc --play-and-exit tmp_audio.mp3")
            os.remove("../tmp_audio.mp3")
            #rimuovere file mp4
        else:
            print("Nessun video trovato per la ricerca:", search_word)

    def download_yt(self, keyword):
        speak("Certo, scarico: " + keyword)
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
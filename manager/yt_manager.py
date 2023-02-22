import pytube
import vlc
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
            yt = pytube.YouTube(video_link).streams.get_audio_only().url
            instance = vlc.Instance()
            player = instance.media_player_new()
            media = instance.media_new(yt)
            media.get_mrl()
            player.set_media(media)
            player.play()
        else:
            print("Nessun video trovato per la ricerca:", search_word)

    def download_yt(self, keyword):
        speak("Certo, scarico: " + keyword)
        search_word = keyword
        results = YoutubeSearch(search_word, max_results=1).to_dict()
        if len(results) > 0:
            #AGGIUNGERE PATH CARTELLA PER PLAYLIST
            video_link = "https://www.youtube.com/watch?v=" + results[0]['id']
            video = pytube.YouTube(video_link)
            video.streams.get_audio_only().download(filename=video.title+".mp3")
        else:
            print("Nessun video trovato per la ricerca:", search_word)
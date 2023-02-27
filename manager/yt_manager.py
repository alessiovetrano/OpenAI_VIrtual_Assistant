import pytube
import vlc
import os
from youtube_search import YoutubeSearch
from manager.tts_manager import speak


class YtManager:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

    def play_yt(self, keyword):
        audio_track = None
        if "playlist" in keyword:
            if not os.path.exists("playlist"):
                speak("Non esiste alcuna playlist da riprodurre")
            else:
                speak("Certo, riproduco la tua playlist")
                for filename in os.listdir("playlist"):
                    audio_track = os.path.join("playlist", filename)
        else:
            speak("Certo, riproduco " + keyword)
            search_word = keyword
            results = YoutubeSearch(search_word, max_results=1).to_dict()
            if len(results) > 0:
                video_link = "https://www.youtube.com/watch?v=" + results[0]['id']
                audio_track = pytube.YouTube(video_link).streams.get_audio_only().url
            else:
                speak("Nessun video trovato per " + search_word)
        if audio_track is not None:
            media = self.instance.media_new(audio_track)
            media.get_mrl()
            self.player.set_media(media)
            self.player.play()

    def download_yt(self, keyword):
        speak("Certo, scarico: " + keyword)
        search_word = keyword
        results = YoutubeSearch(search_word, max_results=1).to_dict()
        if len(results) > 0:
            video_link = "https://www.youtube.com/watch?v=" + results[0]['id']
            video = pytube.YouTube(video_link)
            video.streams.get_audio_only().download(output_path="playlist", filename=video.title + ".mp3")
        else:
            speak("Nessun video trovato per " + search_word)

    def manager_audio(self, keyword):
        if self.player.get_media() is None:
            return
        if "pausa" or "stoppa" or "stop" in keyword:
            self.player.pause()
        elif "play" or "rimetti" in keyword:
            self.player.play()

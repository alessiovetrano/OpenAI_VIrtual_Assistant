import pytube
import vlc
import os
from youtube_search import YoutubeSearch
from manager.tts_manager import speak


class YtManager:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.playlist = []
        self.current_track_index = -1

    def play_yt(self, keyword):
        audio_track = None
        if "playlist" in keyword:
            if not os.path.exists("playlist"):
                speak("Non esiste alcuna playlist da riprodurre")
            else:
                speak("Certo, riproduco la tua playlist")
                self.playlist = [os.path.join("playlist", filename) for filename in os.listdir("playlist")]
                self.current_track_index = 0
                self.play_current_track()
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
        speak("Certo, scarico " + keyword)
        search_word = keyword
        results = YoutubeSearch(search_word, max_results=1).to_dict()
        if len(results) > 0:
            video_link = "https://www.youtube.com/watch?v=" + results[0]['id']
            video = pytube.YouTube(video_link)
            video.streams.get_audio_only().download(output_path="playlist", filename=video.title + ".mp3")
            speak("Il download è stato completato con successo")
        else:
            speak("Nessun video trovato per " + search_word)

    def play_current_track(self):
        if not self.playlist:
            return
        audio_track = self.playlist[self.current_track_index]
        media = self.instance.media_new(audio_track)
        media.get_mrl()
        self.player.set_media(media)
        self.player.play()

    def play_next_track(self):
        if not self.playlist:
            return
        if self.current_track_index < len(self.playlist) - 1:
            self.current_track_index += 1
            self._play_current_track()
        else:
            self.player.stop()

    def play_previous_track(self):
        if not self.playlist:
            return
        if self.current_track_index > 0:
            self.current_track_index -= 1
            self._play_current_track()
        else:
            self.current_track_index = 0
            self._play_current_track()

    def manager_audio(self, keyword):
        if self.player.get_media() is None:
            return
        if "pausa" in keyword or "stoppa" in keyword or "stop" in keyword:
            self.player.pause()
        elif "play" in keyword or "rimetti" in keyword:
            self.player.play()
        elif "prossima" in keyword:
            self.play_next_track()
        elif "precedente" in keyword:
            self.play_previous_track()


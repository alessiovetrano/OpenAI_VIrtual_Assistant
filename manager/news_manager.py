
from manager.tts_manager import speak
import requests
API_KEY = '8bd50ac5cef82f3b0da32a92091ac7bf'


class NewsManager:

    def ask_news(self):
        url = 'https://gnews.io/api/v4/search?q=notizie&lang=it&country=it&token=8bd50ac5cef82f3b0da32a92091ac7bf'
        response = requests.get(url)
        data = response.json()
        for article in data['articles'][:5]:
            speak('Titolo:' + article['title'])
            speak('Descrizione:' + article['description'])
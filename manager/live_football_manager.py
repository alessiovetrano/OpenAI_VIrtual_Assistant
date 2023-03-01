import requests
from manager.tts_manager import speak

class LiveFootball:

    def __init__(self):
        self.url = "https://v3.football.api-sports.io/fixtures?live=all"
        self.headers = {
            "x-rapidapi-host": "v3.football.api-sports.io",
            "x-rapidapi-key": "1da9713a81ed3bb325b364715ffb34ca"
        }

    def get_match(self, team_name):
        team_name = team_name.capitalize()
        response = requests.get(self.url, headers=self.headers)
        data = response.json()

        for fixture in data["response"]:
            home_team = fixture["teams"]["home"]["name"]
            away_team = fixture["teams"]["away"]["name"]
            if team_name in [home_team, away_team]:
                home_score = fixture['goals']['home']
                away_score = fixture['goals']['away']
                speak(f"Il risultato attuale è {home_team} {home_score} {away_team} {away_score}")
            else:
                print("Nessuna squadra")

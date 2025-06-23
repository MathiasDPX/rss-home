from datetime import datetime
from classes import *
from os import getenv
import requests
import pytz

SUMMONER = "T2CS23HgmPZnbRSBItmoO58XZ1k3EzGD-kkKZuTjqFGrcE1IAIg2wThn6JWclRWq23iRZCAKW4tP7A"
BASE_URL = "https://europe.api.riotgames.com"

def formatUnix(timestamp):
    dt_utc = datetime.fromtimestamp(timestamp//1000, tz=pytz.timezone("Europe/Paris"))
    return dt_utc.strftime("%d/%m %H:%M")

class LoL(Provider):
    def __init__(self, conn):
        super().__init__(conn, "lol", self.fetch)
        self.cur.execute("CREATE TABLE IF NOT EXISTS lol (id VARCHAR(255) PRIMARY KEY NOT NULL);")

        self._headers = {
            "X-Riot-Token": getenv("lol_token")
        }

    def get_matches(self):
        r = requests.get(BASE_URL+f"/lol/match/v5/matches/by-puuid/{SUMMONER}/ids", headers=self._headers)
        return r.json()

    def get_match(self, match_id):
        r = requests.get(BASE_URL+f"/lol/match/v5/matches/{match_id}", headers=self._headers)
        return r.json()

    def fetch(self):
        matches = self.get_matches()
        articles = []

        for match in matches:
            if type(match) != str:
                return [] # dont look like a match list, return nothing
            
            self.cur.execute("SELECT 1 FROM lol WHERE id=%s", (match, ))
            if self.cur.fetchone() != None:
                continue # already scraped, skip
            
            matchInfo = self.get_match(match)
            participants = matchInfo['info']['participants']
            startTimestamp = matchInfo['info']['gameStartTimestamp']

            for participant in participants:
                if participant["puuid"] != SUMMONER:
                    continue
                
                informations = {}

                informations['Lane'] = participant['lane']
                informations['KDA'] = f"{participant['kills']}/{participant['deaths']}/{participant['assists']}"
                informations['Champion'] = participant['championName']
                informations['Damage dealt'] = participant['totalDamageDealt']
                informations['Damage taken'] = participant['totalDamageTaken']
                informations['CS'] = participant['totalMinionsKilled']
                informations['Result'] = "win" if participant['win'] else "lose"

                description = "\n".join(f"{k}: {v}" for k,v in informations.items())

                if participant['gameEndedInSurrender']:
                    description += "\nsurrendered"

                article = Article(
                    f"LoL match of {formatUnix(startTimestamp)}",
                    description
                )

                self.cur.execute("INSERT INTO lol VALUES (%s)", (match, ))
                articles.append(article)

        return articles

providers = [LoL]
from classes import *
from os import getenv
import requests

UID="He6Vzxmi"

"""
Modrinth PAT scopes:
- Read notifications

https://modrinth.com/settings/pats
"""

class Modrinth(Provider):
    def __init__(self, conn):
        super().__init__(conn, "modrinth", self.fetch)
        self.cur.execute("CREATE TABLE IF NOT EXISTS modrinth (id VARCHAR(255) PRIMARY KEY NOT NULL);")
        self._headers = {
            "Authorization": "Bearer "+getenv("modrinth_pat")
        }

    def getNotifications(self):
        r = requests.get(f"https://api.modrinth.com/v2/user/{UID}/notifications", headers=self._headers)
        return r.json()

    def fetch(self):
        articles = []
        notifications = self.getNotifications()

        for notif in notifications:
            self.cur.execute("SELECT 1 FROM modrinth WHERE id=%s;", (notif["id"], ))
            if self.cur.fetchone() == None:
                self.cur.execute("INSERT INTO modrinth VALUES (%s);", (notif["id"], ))
                articles.append(Article(
                    notif['title'],
                    notif['text']
                ))

        return articles

providers = [Modrinth]
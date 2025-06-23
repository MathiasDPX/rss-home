from classes import *
from os import getenv
import requests

class HackClub(Provider):
    def __init__(self, conn):
        super().__init__(conn, "hc-mails", self.fetch)
        self.cur.execute("CREATE TABLE IF NOT EXISTS mails (id VARCHAR(255) PRIMARY KEY NOT NULL, type VARCHAR(255), status VARCHAR(255), tracking_number VARCHAR(255), title VARCHAR(255));")
        self.BASE_URL = "https://mail.hackclub.com"
        self._headers = {
            "Authorization": "Bearer "+getenv("hc-mails_token")
        }

    def fetch(self):
        articles = []

        r = requests.get(f"{self.BASE_URL}/api/public/v1/mail", headers=self._headers)
        mails = r.json()["mail"]

        for mail in mails:
            self.cur.execute("SELECT * FROM mails WHERE id=%s;", (mail['id'], ))
            data = self.cur.fetchone()
            if data == None:
                print(f"New mail! {mail['id']}")
                self.cur.execute("INSERT INTO mails VALUES (%s, %s, %s, %s, %s);", (
                    mail.get("id"),
                    mail.get("type", "unknown"),
                    mail.get("status", "unknown"),
                    mail.get("tracking_number"),
                    mail.get("title")
                ,))
                continue

            text = ""
            if data.get("status") != mail.get("status"):
                text += f"Status changed to '{mail.get('status')}'\n"
                self.cur.execute("UPDATE mails SET status=%s WHERE id=%s;", (mail.get('status'), mail['id']))

            if data.get("tracking_number") != mail.get("tracking_number"):
                tracking_num = mail.get("tracking_number")
                if tracking_num == None:
                    continue
                text += f"Tracking available {tracking_num}\n"

            if text != "":
                article = Article(
                    mail.get("title", mail.get("id", "unknown mail")),
                    text.strip("\n")
                )
                articles.append(article)

        return articles

providers = [HackClub]
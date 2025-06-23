from classes import *
import requests
import atoma

CHANNELS = [
    "UCK6vQTUwSzUao8zpVvweavQ",
    "UCZXW8E1__d5tZb-wLFOt8TQ",
    "UCoXVOBqi23uM7SRXE5-0eZA"
]

class YouTube(Provider):
    def __init__(self, conn):
        super().__init__(conn, "youtube", self.fetch)
        self.cur.execute("CREATE TABLE IF NOT EXISTS youtube (id VARCHAR(255) PRIMARY KEY NOT NULL);")

    def fetch_channel(self, id) -> Article:
        desc = ""
        r = requests.get(f"https://www.youtube.com/feeds/videos.xml?channel_id={id}")
        feed = atoma.parse_atom_bytes(r.content)
        for entry in feed.entries:
            self.cur.execute("SELECT * FROM youtube WHERE id=%s", (entry.id_, ))
            if self.cur.fetchone() == None:
                desc += f"<p>- {entry.title.value}</p>"
                self.cur.execute("INSERT INTO youtube VALUES (%s)", (entry.id_, ))

        return Article(
            f"{feed.authors[0].name}'s videos",
            desc
        )

    def fetch(self):
        videos = []
        
        for channel in CHANNELS:
            article = self.fetch_channel(channel)
            if article.description != "":
                videos.append(article)

        return videos

providers = [YouTube]
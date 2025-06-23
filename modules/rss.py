from classes import *
import feedparser

FEEDS = [
    "https://blog.cloudflare.com/rss/",
]

class GenericRSS(Provider):
    def __init__(self, conn):
        super().__init__(conn, "generic-rss", self.fetch)
        self.cur.execute("CREATE TABLE IF NOT EXISTS generic_rss (id VARCHAR(255) NOT NULL, source VARCHAR(255));")

    def fetch(self):
        articles = []

        for feed in FEEDS:
            data = feedparser.parse(feed)
            title = data.feed.title

            for entry in data.entries:
                self.cur.execute("SELECT 1 FROM generic_rss WHERE id=%s AND source=%s", (entry.id, title, ))
                if self.cur.fetchone() == None:
                    articles.append(Article(
                        entry.title,
                        entry.description
                    ))

                    self.cur.execute("INSERT INTO generic_rss VALUES (%s, %s)", (entry.id, title, ))

        return articles

providers = [GenericRSS]
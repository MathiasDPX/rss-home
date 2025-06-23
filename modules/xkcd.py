from classes import *
import requests
import atoma
import re

def get_id_from_url(url):
    match = re.search('xkcd.+\/(\d+)', url).group(1)
    if match.isdigit():
        return str(match)
    return "????"

class XKCD(Provider):
    def __init__(self, conn):
        super().__init__(conn, "xkcd", self.fetch)
        self.cur.execute("CREATE TABLE IF NOT EXISTS xkcd (id INT PRIMARY KEY NOT NULL);")

    def fetch(self):
        articles = []
        r = requests.get("https://xkcd.com/atom.xml")
        feed = atoma.parse_atom_bytes(r.content)
        for post in feed.entries:
            date = post.updated
            url = post.links[0].href
            id = get_id_from_url(url)

            self.cur.execute("SELECT * FROM xkcd WHERE id=%s;", (id, ))
            if self.cur.fetchone() == None:
                self.cur.execute("INSERT INTO xkcd VALUES (%s);", (id, ))
                articles.append(Article(
                    f"xkcd {id}",
                    f"'{post.title.value}' available at {url}"
                ))

        return articles

providers = [XKCD]
from classes import *
import requests
import atoma

class jvns(Provider):
    def __init__(self, conn):
        super().__init__(conn, "jvns", self.fetch)
        self.cur.execute("CREATE TABLE IF NOT EXISTS jvns (id VARCHAR(255) PRIMARY KEY NOT NULL);")

    def fetch(self):
        r = requests.get("https://jvns.ca/atom.xml")
        feed = atoma.parse_atom_bytes(r.content)
        desc = ""
        for post in feed.entries:
            id = post.id_

            self.cur.execute("SELECT * FROM jvns WHERE id=%s;", (id, ))
            if self.cur.fetchone() == None:
                self.cur.execute("INSERT INTO jvns VALUES (%s);", (id, ))
                desc += "<p>- "+post.title.value+"</p>"

        if desc == "":
            return []
        
        return [Article("Julia Evans blog post", desc.strip("\n"))]

providers = [jvns]
class Article:
    def __init__(self, title:str, description:str):
        self.title = title
        self.description = description

    def __repr__(self):
        return f"<Article id='{self.title}'>"
    
class Provider:
    def __init__(self, conn, name:str, fetch_function):
        self.fetch_function = fetch_function
        self.cur = conn.cur
        self.conn = conn
        self.name = name

    def __repr__(self):
        return f"<Provider name='{self.name}'>"
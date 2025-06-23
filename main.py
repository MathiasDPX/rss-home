from dotenv import load_dotenv
from database import *
from classes import *
import importlib
import requests
import imgkit
import glob

load_dotenv(".env")

modules = glob.glob("modules/*.py")
conn = DatabaseConnection()

if __name__ == "__main__":
    news = []
    all_providers = []

    # MARK: List modules
    for path in modules:
        module = importlib.import_module(path[:-3].replace("\\", "."))
        if hasattr(module, "providers") == False:
            name = path.replace('modules\\', '')
            print(f"Unable to find providers for {name}")
            continue

        providers = module.providers

        for provider in providers:
            if provider not in Provider.__subclasses__():
                print(f"Invalid provider '{provider.__name__} in {path}'")
                continue
            
            if not hasattr(provider, "fetch"):
                print(f"Provider '{provider.__name__}' don't contain a function 'fetch'")
                continue

            all_providers.append(provider)

    # MARK: Get news
    for provider in all_providers:
        prov = provider(conn)

        if getenv(f"PROVIDER_{prov.name}", "false").lower() == "false":
            print(f"[X] {prov.name}")
            continue
        else:
            print(f"[✓] {prov.name}")

        prov_news = prov.fetch()

        if type(prov_news) != list:
            print(f"Invalid response from '{provider.__name__}' (expected list got {type(prov_news).__name__})")
            continue

        if not all(isinstance(item, Article) for item in prov_news):
            print(f"All items from '{provider.__name__}' aren't Article")
            continue

        news.extend(prov_news)

    if len(news) == 0:
        exit("No news found")

    # MARK: Render

    # Discord webhook
    if getenv("discord_webhook", "false").lower() != "false":
        fields = []

        for new in news:
            fields.append({
                "name": new.title,
                "value": new.description,
                "inline": True
            })

        data = {"embeds":[{"fields": fields}]}
        r = requests.post(getenv("discord_webhook"), json=data)

    # Catprinter (partially done)
    if getenv("catprinter", "false").lower() != "false":
        innerHTML = ""
        for new in news:
            description = new.description
            description = description.replace("\n", "<br>")
            innerHTML += f"<b>{new.title}</b><br><p>{description}</p><br>"

        innerHTML = "<style>@import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100..900;1,100..900&display=swap');*{font-family:\"Roboto\",sans-serif;padding:0px;margin:0px;}p{padding-left:1.5em;text-indent:-0.6em;}</style><div>"+innerHTML[:-4]+"</div>"

        imgkit.from_string(innerHTML, 'image.png', options={
            "width": 384
        })

    # Slack webhook
    if getenv("slack_webhook", "false").lower() != "false":
        fields = []

        for new in news:
            fields.append({
                "title": new.title,
                "value": new.description
            })

        payload = {"attachments": [{"fields":fields}]}
        r = requests.post(getenv("slack_webhook"), json=payload)
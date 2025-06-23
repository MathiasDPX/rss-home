# RSS Home
A RSS aggregator for Discord, Slack or saycheese's printer

Available services:
- Julia Evans's blog
- Hackclub Mails
- Generic RSS
- XKCD
- YouTube videos
- LoL matches recap

Available outputs:
- Discord
- Slack
- Image (for thermal printer)


## Installation

### .env
Before starting rss-home, you need to add postgres credentials and enable some providers. You also need to add a webhook url for Discord/Slack

### Running
A simple crontab running every 15/30 minutes

```
*/10 * * * * cd /home/you/rsshome && /home/you/rsshome/.venv/Scripts/python main.py
```
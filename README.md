# RSS Home
rss-home is a content aggregation and distribution system for news feeds, videos, blogs, and notifications.

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
- Saycheese printer (soon)

## Installation

### 1. Clone the repository
```
git clone https://github.com/MathiasDPX/rss-home
```

### 2. Setup .env
```
mv env.example .env
```
1. You need to setup a PostgreSQL database for saving already sent news, you can use Nest
2. By default, all providers are disabled, for enabling them, change `false` to `true` in the Providers section. Some providers (like generic-rss or YouTube) need a deeper configuration that can be found in their respective file.
3. Discord & Slack are the only output currently supported, for enabling them you need to change `false`

### 3. Install a venv
```
python -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies
```
pip install -r requirements.txt
```

### 5. Setup cronjob
```
crontab -e

// Then, on a new line
*/10 * * * * cd /home/you/rsshome && /home/you/rsshome/.venv/bin/python main.py
```

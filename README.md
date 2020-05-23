# Telerona

🦠 A coronavirus tracker bot for Telegram.

## Deploy the bot

### Deploy on Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### Deploy yourself

#### Preparation

1. Rename `.env.sample` file to `.env`
2. Open `.env` file and fill in the fields

```ini
API_ID=1234567
API_HASH=0apz3jxk603w5mno6a6p6cg27lzgsrfq
BOT_TOKEN=1234567890:ABC-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DATABASE_URL= postgres://xzy
```

#### Installation

```sh
pip3 install -r requirements.txt
python3 -m telerona
```

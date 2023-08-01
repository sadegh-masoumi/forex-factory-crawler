import requests


class Telegram:
    URL = "https://api.telegram.org/bot{BOT_API_KEY}/sendMessage?chat_id={CHAT_ID}&text={message}"

    def __init__(self, token, chat_id) -> None:
        self.URL = self.URL.format(BOT_API_KEY=token, CHAT_ID=chat_id)

    def send_message(self, message):
        res = requests.get(self.URL.format(message=message))
        return res
import requests


class Telegram:
    URL = (
        "https://api.telegram.org/bot{BOT_API_KEY}/sendMessage?chat_id={CHAT_ID}&text="
    )

    def __init__(self, token: str, chat_id: int) -> None:
        self.URL = self.URL.format(BOT_API_KEY=token, CHAT_ID=chat_id)

    def send_message(self, message: str):
        res = requests.get(self.URL + message)
        return res

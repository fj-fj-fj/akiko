import json
from logging import Logger
from typing import Any, Dict

from api.coinmarketcap.core import CoinDataFetcher
from db import shelve_db
from config.webhook import configurate_webhook

logger: Logger = Logger(__file__)


class Bot(CoinDataFetcher):

    _CALLBACK_QUERY_ID: int = 0

    def __init__(self, **kwargs: dict) -> None:
        super().__init__(**kwargs["coinmarketcap"])

        for key, value in kwargs["bot"].items():
            setattr(Bot, key, value)

    def update_webhook(self) -> None:
        configurate_webhook(self)

    def send_message(self, chat_id: int, text: str) -> Dict[str, Any]:
        """
        This method sends to user a message.

        Args:
            chat_id: chat ID

        Returns:
            message: Coin price (and/or information), or some error

        """
        logger.debug(f"{chat_id=}, {text=}")

        url = Bot.URL + "sendMessage"
        data = {"chat_id": chat_id, "text": ""}

        if Bot._CALLBACK_QUERY_ID or "error" in text:
            data["text"] += text
            Bot._CALLBACK_QUERY_ID = 0
            return self.session.post(url, json=data).json()

        if "Akiko" in text:
            data["parse_mode"] = "markdown"
            data["text"] += f"{text}{'(‾◡◝)':>40}"
            return self.session.post(url, json=data).json()

        if "$" in text:
            bitcoin_fetched = shelve_db.fetch_last_coin_id(chat_id) == 1
            data["parse_mode"] = "markdown"
            data["text"] += text
            data["reply_markup"] = {
                "inline_keyboard": [
                    [
                        {
                            "text": "฿uy" if bitcoin_fetched else "Buy",
                            "callback_data": "In the near future you can do it",
                        }
                    ]
                ]
            }
            return self.session.post(url, json=data).json()

        text = json.loads(text)
        data["disable_web_page_preview"] = True

        id_coin, name_coin = text.pop("🗝")

        if name_coin == "GoHelpFund":
            data[
                "text"
            ] += "HELP it's GoHelpFund ticker\n \
                             Enter /help or h if you need help\n\n"

        for key, value in text.items():
            if not value:
                continue  # noqa: E701
            value = " | ".join([i for i in value])
            data["text"] += key + " - " + value + "\n\n"

        kiss = "H( ^ _ - )DL" if id_coin == 1 else "it's altc(´◡`)in"
        data["text"] += kiss

        return self.session.post(url, json=data).json()

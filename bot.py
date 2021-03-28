# -*- coding: utf-8 -*-

"""This module contains class Bot"""

import json
import time
import sys

from api.coinmarketcap.core import CoinDataFetcher
from db import shelve_db


class Bot(CoinDataFetcher):
    _CALLBACK_QUERY_ID = 0

    def __init__(self, **kwargs: dict) -> None:
        super().__init__(**kwargs['coinmarketcap'])

        for key, value in kwargs['bot'].items():
            setattr(Bot, key, value)

    def webhook(self):
        """This function first gets the getWebhookinfo object. 
        Then it gets the webhook URL from it, which can be empty. 
        Then he checks the machine for localization. If it is a working host, 
        checks for a webhook URL and hangs a hook to continue development. 
        Or installs a webhook on a remote server if it was removed for some reason, 
        but the development is not underway.

        """
        r = self.session.get(f'{Bot.URL}getwebhookinfo').json()
        print(f'\nBot.webhook response: {r}', file=sys.stderr)
        
        is_webhook = r['result']['url']
        for_incoming_updates = f'{Bot.URL}setWebhook'

        if Bot.IS_LOCALHOST:
            from utils import tunnel as t

            if is_webhook == t.TUNNEL_URL:
                print('\tis session TUNNEL_URL', file=sys.stderr)
                return

            self.session.get(Bot.URL + 'deleteWebhook')
            time.sleep(0.2)
            r = self.session.get(for_incoming_updates, params={'url': t.TUNNEL_URL})
            print(f'\t\tsetWebhook -> TUNNEL_URL: {r.json()}', file=sys.stderr)
            return

        if is_webhook == Bot.APP_NAME:
            print('\tis session APP_NAME', file=sys.stderr)
            return

        self.session.get(Bot.URL + 'deleteWebhook')
        time.sleep(0.2)
        r = self.session.get(for_incoming_updates, params={'url': Bot.APP_NAME})
        print(f'\t\tsetWebhook -> APP_NAME: {r.json()}', file=sys.stderr)
        return


    def send_message(self, chat_id: int, text: str) -> str:
        """The funcion sends users a message.

        :param chat_id: (int)chat ID
        :param: (str)text: coin price and/or coin information, or error message 
        :return: (dict)requests.models.Response

        """
        print(f'\nBot.send_message(chat_id={chat_id}, text={text})\n', file=sys.stderr)

        url = Bot.URL + 'sendMessage'
        data = {
            'chat_id': chat_id, 
            'text': ''
        }
        
        if Bot._CALLBACK_QUERY_ID or 'error' in text:
            data['text'] += text
            r = self.session.post(url, json=data)
            Bot._CALLBACK_QUERY_ID = 0
            return r.json()
        
        if 'Akiko' in text:
            data['parse_mode'] = 'markdown'
            data['text'] += f"{text}{'(‾◡◝)':>40}"
            r = self.session.post(url, json=data)
            return r.json()

        if '$' in text:
            data['parse_mode'] = 'markdown'
            data['text'] += text
            data['reply_markup'] = {
                    'inline_keyboard': [
                        [{'text': '฿uy' if shelve_db.fetch_last_coin_id(chat_id) == 1 else 'Buy',
                          'callback_data': 'In the near future you can do it'}]
                    ]
            }
            r = self.session.post(url, json=data)
            return r.json()

        text = json.loads(text)
        data['disable_web_page_preview'] = True

        id_coin, name_coin = text.pop('🗝')

        if name_coin == "GoHelpFund":
            h = 'HELP it\'s GoHelpFund ticker\nEnter /help or h if you need help\n\n'
            data['text'] += h

        for key, value in text.items():
            if not value: continue
            value = ' | '.join([i for i in value])
            data['text'] += key + ' ▫️ ' + value + '\n\n'

        kiss = 'H( ^ _ - )DL' if id_coin == 1 else "it's altc(´◡`)in"
        data['text'] += kiss

        r = self.session.post(url, json=data)
        
        return r.json()

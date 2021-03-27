# -*- coding: utf-8 -*-

"""This module contains class Coinmarketcap"""

import sys
import json
import requests

try:
    from misc import CMC_PRO_API_KEY
except (ModuleNotFoundError, ImportError):
    import os

    CMC_PRO_API_KEY = os.environ.get('CMC_PRO_API_KEY')


class Coinmarketcap:
    """Class contains methods for working with coinmarketcap API"""

    _URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/'


    def __init__(self):
        """request headers and session are initialized"""

        self.session = requests.Session()
        self.session.headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'X-CMC_PRO_API_KEY': CMC_PRO_API_KEY
        }


    def get_price(self, id_coin: int) -> str:
            """
                This function searches for a coin by ID and 
                (if successful) formats the result in monospaced font

                :param id_coin: (int)coin ID
                :return: (str)coin price

                user [in]: Monero
                Akiko [out]: $  `122.05317918661694`

            """
            url = f'{Coinmarketcap._URL}quotes/latest?id={id_coin}'
            r = self.session.get(url).json()

            price = str(r['data'][str(id_coin)]['quote']['USD']['price'])
            answer = f'$  `{price}`'

            print(f'\nCoinmarketcap.get_price({id_coin}) -> {answer}', file=sys.stderr)
            return answer


    def get_coin_id(self, message: str): # -> int or None
        """
            This function searches for a coin by
            its name or ticker and if it finds it returns it

            :param message: (str)user entered text 
            :return: (int)coin price or None

        """
        url = f'{Coinmarketcap._URL}map'
        r = self.session.get(url).json()

        for coin in r["data"]:
            name = coin["name"].lower()
            symbol = coin["symbol"].lower()

            if message in [name, symbol]:
                id_coin = coin["id"]

                print(f'\nCoinmarketcap.get_coin_id({message}) -> {id_coin}', file=sys.stderr)
                return id_coin

        print(f'\nCoinmarketcap.get_coin_id({message}) -> {None}', file=sys.stderr)


    def get_info(self, id_coin: int) -> str:
        """
            This function collects some informaion about the <entered_coin>
            such as: links to website, social networks, exoplorers, tech doc, sourc code.

            :param id_coin: (id)coin ID
            :return: (str)links 
            
        """
        url = f'{Coinmarketcap._URL}info?id={id_coin}'
        r = self.session.get(url).json()

        links = r['data'][next(iter(r['data']))]['urls']  # e.g. btc - "data": {"1": {...
        name_coin = r['data'][next(iter(r['data']))]['name']
        links['🗝'] = id_coin, name_coin
        links = json.dumps(links)

        print(f'\nCoinmarketcap.get_info({id_coin}) -> {links}', file=sys.stderr)
        return links

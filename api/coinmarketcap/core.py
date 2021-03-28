"""
This module contains class CoinDataFetcher.

"""
import json
from logging import Logger
from requests import Session
from typing import Any, Dict, Optional


class CoinDataFetcher:

    """Class contains methods for working with Coinmarketcap API."""

    def __init__(self, **config_kw) -> None:
        self.logger: Logger = Logger(__file__)
        self.session: Session = Session()
        self.session.headers = config_kw['headers']
        self.coinmarketcap_url = config_kw['url']
        self.timeout = config_kw['timeout']
                    
    def extract_coin_price(self, coin_ID: int) -> str:
        """This endpoint searches a coin by ID and returns it if exists.

        Args:
            Coin ID

        Returns:
            Coin price with monospaced font
            Example:
                user [in]: Monero
                Akiko [out]: $  `219.5910124308485`

        """
        url: str = f'{self.coinmarketcap_url}quotes/latest?id={coin_ID}'
        r: Dict[str, Any] = self.session.get(url, timeout=self.timeout).json()

        price = str(r['data'][str(coin_ID)]['quote']['USD']['price'])
        answer: str = f'$  `{price}`'

        self.logger.debug(f'Coin ID:{coin_ID}, Price:{answer}')
        return answer

    def fetch_coin_id(self, message: str) -> Optional[int]:
        """
        This endpoint searches a Coin by its name or ticker
        and returns it if exists.

        Args:
            User entered text

        Returns:
            Coin price or None

        """
        url: str = f'{self.coinmarketcap_url}map'
        r: Dict[str, Any] = self.session.get(url, timeout=self.timeout).json()

        for coin in r["data"]:
            name = coin["name"].lower()
            symbol = coin["symbol"].lower()

            if message in (name, symbol):
                coin_id = coin["id"]
                self.logger.debug(f'Message:{message} with Coin ID:{coin_id}')
                return coin_id

        self.logger.debug(f'Message:{message} with Coin ID:None')

    def display_coin_info(self, coin_id: int) -> str:
        """
        This endpoint diaplays info about the entered Coin such as:
        links to website, social networks, exoplorers, tech doc, sourc code.

        """
        url: str = f'{self.coinmarketcap_url}info?id={coin_id}'
        r: Dict[str, Any] = self.session.get(url, timeout=self.timeout).json()

        links = r['data'][next(iter(r['data']))]['urls']  # e.g. btc - "data": {"1": {... # noqa E501
        name_coin = r['data'][next(iter(r['data']))]['name']
        links['🗝'] = coin_id, name_coin

        self.logger.debug(f'Coin ID:{coin_id} with links:\n{coin_id}')
        return json.dumps(links)

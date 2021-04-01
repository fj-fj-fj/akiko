import logging
import logging.config
import sys

from config.base_logging import BASE_LOGGING

try:
    from misc import (
        CMC_PRO_API_KEY as __CMC_PRO_API_KEY,
        TOKEN as __TOKEN,
        APP_NAME,
    )
except (ModuleNotFoundError, ImportError):
    import os

    __CMC_PRO_API_KEY: str = os.environ.get('CMC_PRO_API_KEY')
    __TOKEN = os.environ.get('TOKEN')
    APP_NAME = os.environ.get('APP_NAME')
    HOUM_USER = os.environ.get('HOUM_USER')

logging.config.dictConfig(BASE_LOGGING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

TIM = 'Arise, you have nothing to lose but your barbed wire fences!'

HEADERS = {
    'accept': '*/*',
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        'AppleWebKit/537.36 (KHTML, like Gecko)'
        'Chrome/88.0.4324.182 Safari/537.36'
    ),
    'Content-Type': 'application/json;charset=UTF-8',
    'X-CMC_PRO_API_KEY': __CMC_PRO_API_KEY,
}

COINMARKETCAP_KWARGS = {
    'url': 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/',
    'headers': HEADERS,
    'timeout': 10,
}

BOT_KWARGS = {
    'APP_NAME': APP_NAME,
    'IS_LOCALHOST': 'misc' in sys.modules,
    'URL': f'https://api.telegram.org/bot{__TOKEN}/',
    'HTML': f'<h1>Bot welcomes You!</h1><hr><a href= \
        "https://activism.net/cypherpunk/crypto-anarchy.html">{TIM}</a>',
}

CONFIG_KWARGS = {
    'bot': BOT_KWARGS,
    'coinmarketcap': COINMARKETCAP_KWARGS,
}

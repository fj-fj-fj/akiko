import re
from logging import Logger
from typing import Optional, Tuple

from db import shelve_db

logger: Logger = Logger(__file__)


def form_response_to_user(bot: object, r: dict) -> Tuple[str, str]:
    info_patterns = 'information /info info i'.split()
    help_patterns = '/start /help h sos'.split()

    try:
        chat_id: str = r['message']['chat']['id']
        message: str = r['message']['text'].lower().strip()

        user_has_session: bool = shelve_db.has_user_session(chat_id)

        user_wants_more_info: bool = message in info_patterns
        user_needs_help: bool = message in help_patterns

        logger.debug(f'{message=}, {user_wants_more_info=}, {user_has_session=}')  # noqa: E501

        if user_wants_more_info and not user_has_session:
            data: str = shelve_db.display_error_message('session')
        elif user_wants_more_info and user_has_session:
            id_coin: int = shelve_db.fetch_last_coin_id(chat_id)
            data: str = bot.display_coin_info(id_coin)
        elif user_needs_help:
            # re because multi-line messages preserve spaces
            data = re.sub(r'((?!\n)\s+)', ' ', """I'm *Akiko* and i use coinmarketcap API\n
                    To get the coin price, send me its name or ticker.
                    (e.g. `Dogecoin` | `Doge`, `Bitcoin` | `BTC`)\n
                    For more information about coin, enter `info` or `i`""")
        else:
            id_coin: Optional[int] = bot.fetch_coin_id(message)
            data = bot.extract_coin_price(id_coin) if id_coin \
                else shelve_db.display_error_message('match')
            shelve_db.touch_session(chat_id, id_coin)  # create or update

    except KeyError:
        bot._CALLBACK_QUERY_ID: str = r['callback_query']['id']
        message: str = r['callback_query']['message']
        chat_id: str = message['chat']['id']
        callback_data: str = message['reply_markup']['inline_keyboard'][0][0]['callback_data']  # noqa: E501

        data: str = callback_data if callback_data else \
            shelve_db.display_error_message('unknown')

        logger.debug(f'{bot._CALLBACK_QUERY_ID=}, {message=}, {data=}')

    return (chat_id, data)

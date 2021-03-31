from logging import Logger
from typing import Tuple

from api.telegram.messages import WELCOME_MESSAGE, display_error_message
from db import shelve_db

logger: Logger = Logger(__file__)


def form_response_to_user(bot: object, r: dict) -> Tuple[str, str]:
    try:
        chat_id: str = r['message']['chat']['id']
        message: str = r['message']['text'].lower().strip()

        data: str = _form_data_response(bot, chat_id, message)
    except KeyError:
        bot._CALLBACK_QUERY_ID: str = r['callback_query']['id']
        message: str = r['callback_query']['message']
        chat_id: str = message['chat']['id']
        callback_data: str = \
            message['reply_markup']['inline_keyboard'][0][0]['callback_data']

        data: str = callback_data if callback_data else \
            display_error_message('unknown')

        logger.debug(f'{bot._CALLBACK_QUERY_ID=}, {message=}, {data=}')

    return (chat_id, data)


def _form_data_response(bot, chat_id, message):
    # type: (object, str, str) -> str
    actions = _define_user_actions(chat_id, message)
    user_has_session, user_wants_more_info, user_needs_help = actions
    logger.debug(f'{chat_id=}, {message=}')

    if user_wants_more_info and not user_has_session:
        data: str = display_error_message('session')
    elif user_wants_more_info and user_has_session:
        id_coin: int = shelve_db.fetch_last_coin_id(chat_id)
        data: str = bot.display_coin_info(id_coin)
    elif user_needs_help:
        data: str = WELCOME_MESSAGE
    else:
        if bot.fetch_coin_id(message):
            data: str = bot.extract_coin_price(id_coin)
        else:
            data: str = display_error_message('match')
        shelve_db.touch_session(chat_id, id_coin)
    return data


def _define_user_actions(chat_id, message):
    # type: (str, str) -> Tuple[bool, bool, bool]
    info_patterns = 'information /info info i'.split()
    help_patterns = '/start /help h sos'.split()

    return(
        shelve_db.has_user_session(chat_id),
        message in info_patterns,
        message in help_patterns,
    )

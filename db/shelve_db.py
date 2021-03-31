"""
Utility functions for work with user sessions and error notifications.

"""
import logging
import shelve
from typing import Optional

__all__ = (
    'touch_session',
    'has_user_session',
    'fetch_last_coin_id',
)

loger = logging.getLogger(__file__)

_SHELVE_DB = 'shelve.db'


def touch_session(chat_id: int, coin_id: Optional[str]) -> None:
    """
    Create a user session or update and save last coin ID.

    """
    loger.debug(f'Chat ID:{chat_id}, Coin ID:{coin_id}')

    if coin_id is None: return  # noqa:E701

    with shelve.open(_SHELVE_DB) as db:
        db[str(chat_id)] = coin_id


def has_user_session(chat_id: int) -> bool:
    """
    Check if the user has a session so that he can fully use the Bot commands.

    """
    loger.debug(f'Chat ID:{chat_id}')

    with shelve.open(_SHELVE_DB) as db:
        klist = list(db.keys())

        return any([key == str(chat_id) for key in klist])


def fetch_last_coin_id(chat_id: int) -> str:
    """
    If the user has a session, it stores the ID of the last coin he entered.
    This case can be used to call this function.

    """
    loger.debug(f'Chat ID:{chat_id}')

    with shelve.open(_SHELVE_DB) as db:
        klist = list(db.keys())
        id_ = {i for i in klist if i == str(chat_id)}.pop()

        return db[id_]

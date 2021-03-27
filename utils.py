# -*- coding: utf-8 -*-

""" 
    * * * app.utils * * *

    Utility functions for work with user sessions and error notifications.

    :touch_session: creates or updates with the user
    :check_user_session: checks for a user session
    :get_last_id_coin: returns coin ID stored in the user session 
    :get_error: returns an error according to the entered data

"""

import shelve
import sys


__all__ = ['touch_session', 'check_user_session', 'get_last_id_coin', 'get_error']


_shelvedb = 'shelve.db'


def touch_session(chat_id: int, id_coin) -> None:
    """Creates a user session or update and saves last coin ID
        key: chat ID, value: id_coin if id_coin is not None

        :param chat_id: (int)chat ID 
        :param id_coin: (int)last coin ID or None

    """
    print(f'\nutils.touch_session(chat_id={chat_id}, \
          id_coin={id_coin}) -> None', file=sys.stderr)

    if id_coin is None: return

    with shelve.open(_shelvedb) as db:
        db[str(chat_id)] = id_coin


def check_user_session(chat_id: int) -> bool:
    """
        Checks if the user has a session
        so that he can fully use the bot commands.

        :param chat_id: (int)user chat ID
        :return: True if user session exists else False

    """
    print(f'\nutils.check_user_session(chat_id=\
          {chat_id}) -> bool\n', file=sys.stderr)

    with shelve.open(_shelvedb) as db:
        klist = list(db.keys())

        return any([key == str(chat_id) for key in klist])


def get_last_id_coin(chat_id: int) -> int:
    """Returns the last coin ID entered by the user.

        If the user has a session, 
        it stores the ID of the last coin he entered.
        This case can be used to call this function
        
        :param chat_id: (int)user chat ID

    """
    print(f'\nutils.get_last_id_coin(chat_id={chat_id}) -> int', file=sys.stderr)

    with shelve.open(_shelvedb) as db:
        klist = list(db.keys())
        id_ = {i for i in klist if i == str(chat_id)}.pop()
        id_coin = db[id_]

        print(f'klist={klist}, len(klist)={len(klist)}', file=sys.stderr)
        return id_coin


def get_error(key: str) -> str:
    """
        This function takes an error type
        and returns an appropriate message.
    
        :param key: (str)error name
        :return: (str)key matching error

    """
    print(f'\nutils.get_error(key={key}) -> str', file=sys.stderr)

    _errors = {
        'session': f"Session error! Enter `Bitcoin` | `btc` or other coin (‾◡◝)",
        'match': r'Match error! ¯\_(ツ)_/¯',
        'unknown': 'Sorry! Unknown error!  ( . .)'
    }

    return _errors[key]

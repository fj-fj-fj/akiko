# -*- coding: utf-8 -*-

"""This module contains app Flask and main function"""

import sys
import re

from flask import Flask
from flask import request
from flask import jsonify

from api.telegram.bot import Bot
from config import CONFIG_KWARGS
from db import shelve_db


app = Flask(__name__)
bot = Bot(**CONFIG_KWARGS)
bot.update_webhook()


@app.route('/', methods=['POST', 'GET'])
def main() -> str:
    """
                        * * * Main function * * *

        If entered correctly (coin name/ticker) returns the price of the coin, 
        otherwise a match error (see self.fetch_coin_id(), self.extract_coin_price())
        When requesting information about a coin, returns links (see self.display_coin_info()) or
        if the coin was not selected a session error

        :return: (str)coin price / coin information / [match/session/unknown] error

    """

    print(' * START main.main() * '.center(130, '~'), file=sys.stderr)

    if request.method == 'POST':

        r = request.get_json()

        try:
            chat_id = r['message']['chat']['id']
            message = r['message']['text'].lower().strip()

            session = shelve_db.has_user_session(chat_id)

            need_more_info = message in ('information', '/info', 'info', 'i')
            need_help = message in ('/start', '/help', 'h', 'sos')

            print(f'main/try: message={message}, need_info={need_more_info}, \
                  session={session}', file=sys.stderr)
                
            if need_more_info and not session:
                data: str = shelve_db.display_error_message('session')
            elif need_more_info and session:
                id_coin: int = shelve_db.fetch_last_coin_id(chat_id)
                data: str = bot.display_coin_info(id_coin)                
            elif need_help:
                # re because multi-line messages preserve spaces
                data = re.sub(r'((?!\n)\s+)', ' ', f"""I'm *Akiko* and i use coinmarketcap API\n
                       To get the coin price, send me its name or ticker.
                       (e.g. `Dogecoin` | `Doge`, `Bitcoin` | `BTC`)\n
                       For more information about coin, enter `info` or `i`""")
            else:
                id_coin = bot.fetch_coin_id(message) # int or None
                data = bot.extract_coin_price(id_coin) if id_coin else shelve_db.display_error_message('match')
                shelve_db.touch_session(chat_id, id_coin) # create or update

        except KeyError:
            bot._CALLBACK_QUERY_ID = r['callback_query']['id']
            message = r['callback_query']['message']
            chat_id = message['chat']['id']
            callback_data = message['reply_markup']['inline_keyboard'][0][0]['callback_data']

            data = callback_data if callback_data else shelve_db.display_error_message('unknown')

            print(f'main/except: click Buy={bot._CALLBACK_QUERY_ID}, \
                  message={message}, data={data}', file=sys.stderr)

        bot.send_message(chat_id, text=data)

        print(f' * FINISH main.main() * \njsonify(r)={jsonify(r)} ', end='\n\n', file=sys.stderr)

        return jsonify(r)

    return bot.HTML


if __name__ == '__main__':
    app.run(debug=bot.IS_LOCALHOST)

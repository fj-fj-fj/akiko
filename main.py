from logging import Logger

from flask import Flask
from flask import request
from flask import jsonify

from api.telegram.bot import Bot
from api.telegram.utils import form_response_to_user
from config import CONFIG_KWARGS

logger: Logger = Logger(__file__)

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

    logger.debug(' * BOT STARTED * '.center(130, '~'))

    if request.method == 'POST':
        r = request.get_json()
        print(type(r))
        chat_id, data = form_response_to_user(bot, r)
        bot.send_message(chat_id, text=data)

        logger.debug(f' * bot FINISHED * \n{jsonify(r)}\n\n')

        return jsonify(r)

    return bot.HTML


if __name__ == '__main__':
    app.run(debug=bot.IS_LOCALHOST)

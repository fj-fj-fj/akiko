from typing import Union

from flask import Flask, Response, jsonify, request

from api.telegram.bot import Bot
from api.telegram.utils import form_response_to_user
from config import CONFIG_KWARGS


app = Flask(__name__)
bot = Bot(**CONFIG_KWARGS)
bot.update_webhook()


@app.route('/', methods=['POST', 'GET'])
def main(bot: object) -> Union[Response, str]:
    if request.method == 'POST':
        r: dict = request.get_json()
        chat_id, data = form_response_to_user(bot, r)
        bot.send_message(chat_id, text=data)
        return jsonify(r)
    return bot.HTML


if __name__ == '__main__':
    app.run(debug=bot.IS_LOCALHOST)

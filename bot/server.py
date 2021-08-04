from flask import request, Flask
from bot import bot
from threading import Thread
from bot.loger import get_logger

app = Flask(__name__)
logger = get_logger(__name__)


@app.route('/bot', methods=['POST'])
def get_webhooks():
    data = request.json['payload']
    x = Thread(target=handle, args=(data,))
    x.start()
    logger.info(data)
    return "ok"


def handle(data):
    if data['type'] == 'message' and data['value']['type'] == 'text':
        text = data['value']['content']['text']
        chat = data['value']['chat_id']
        user = data['value']['user_id']
        author = data['value']['author_id']
        if user != author:
            bot.message_handler(chat, user, text)

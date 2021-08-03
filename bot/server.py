from flask import request, Flask
from bot import bot

app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def get_webhooks():
    data = request.json['payload']
    print(data)
    if data['type'] == 'message':
        text = data['value']['content']['text']
        chat = data['value']['chat_id']
        user = data['value']['user_id']
        author = data['value']['author_id']
        if user != author:
            bot.message_handler(chat, user, text)
        else:
            print("avito kaif")
    return "ok"

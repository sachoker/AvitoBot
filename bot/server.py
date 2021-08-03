from flask import Flask, request
from __init__ import app, bot


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
            bot.read_chat(chat, user)
            bot.message_handler(chat, user, text)
        else:
            print("avito kaif")
    return "ok"

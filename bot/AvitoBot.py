import collections
from requests import get, post
from time import sleep
from bot.loger import get_logger
from json import JSONDecodeError


class AvitoBot:
    def __init__(self, client_id, client_secret, generator, base):
        self.client_id = client_id
        self.client_secret = client_secret
        self.logger = get_logger(__name__)
        self.avitoapikey = None
        self.get_avito_key()
        self.names = []
        self.base = base

        #'169306001'
        for i in self.get_all_chats('204902716'):
            self.names.append(i['id'])
        self.handlers = collections.defaultdict(generator)

    def get_avito_key(self):
        try:
            resp = get(
                f'https://api.avito.ru/token/?grant_type=client_credentials&client_id={self.client_id}&client_secret={self.client_secret}').json()
        except JSONDecodeError:
            self.logger.error('JSONDecodeError on get_avito_key')
            resp = get(
                f'https://api.avito.ru/token/?grant_type=client_credentials&client_id={self.client_id}&client_secret={self.client_secret}').json()
        self.avitoapikey = resp["access_token"]
        self.logger.info(resp)

    def get_webhooks(self):
        avitowebhook = 'https://api.avito.ru/messenger/v2/webhook'
        header = {'Authorization': 'Bearer ' + self.avitoapikey}
        payload = {'url': 'http://3064ce44248a.ngrok.io/bot'}
        resp = post(avitowebhook, headers=header, json=payload)
        self.logger.info(resp)

    def send_message(self, chat_id, user_id, text):
        header = {'Authorization': 'Bearer ' + self.avitoapikey}
        payload = {"type": "text", "message": {"text": text}}
        ans = post(f"https://api.avito.ru/messenger/v1/accounts/{user_id}/chats/{chat_id}/messages", headers=header,
                   json=payload)
        self.logger.info(ans)

    def message_handler(self, chat_id, user_id, text):
        if chat_id in self.handlers.keys():
            try:
                answer = self.handlers[chat_id].send(text)
            except StopIteration:
                del self.handlers[chat_id]
                return self.message_handler(chat_id, user_id, text)
        else:
            answer = next(self.handlers[chat_id])
        self.send_message(chat_id, user_id, answer)
        return 1

    def read_chat(self, chat_id, user_id):
        header = {'Authorization': 'Bearer ' + self.avitoapikey}
        post(f'https://api.avito.ru/messenger/v1/accounts/{user_id}/chats/{chat_id}/read', headers=header)

    def get_all_chats(self, user_id):
        header = {'Authorization': 'Bearer ' + self.avitoapikey}
        chats = get(f'https://api.avito.ru/messenger/v1/accounts/{user_id}/chats', headers=header).json()['chats']
        return chats

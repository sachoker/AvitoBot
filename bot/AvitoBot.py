import collections
from requests import get, post
from time import sleep
from bot.loger import get_logger
from json import JSONDecodeError


class AvitoBot:
    def __init__(self, client_id, client_secret, generator, base):
        self.client_id = client_id
        self.client_secret = client_secret
        self.sdek_client_id = ''
        self.sdek_client_secret = ''
        self.postal_from = ''
        self.sdek_key = None
        # self.get_sdek_key()
        self.logger = get_logger(__name__)
        self.avitoapikey = None
        self.get_avito_key()
        self.names = []
        self.base = base
        # '204902716'
        for i in self.get_all_chats('169306001'):
            self.names.append(i['id'])
        self.names.remove('u2i-2191175409-187456116')
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
        payload = {'url': 'http://99b11ff9a78e.ngrok.io/bot'}
        resp = post(avitowebhook, headers=header, json=payload)
        self.logger.info(resp)

    def send_message(self, chat_id, user_id, text):
        header = {'Authorization': 'Bearer ' + self.avitoapikey}
        payload = {"type": "text", "message": {"text": text}}
        ans = post(f"https://api.avito.ru/messenger/v1/accounts/{user_id}/chats/{chat_id}/messages", headers=header,
                   json=payload)
        self.logger.info(ans)

    def message_handler(self, chat_id, user_id, text):
        self.logger.info(text)
        if chat_id in self.names:
            pass
        elif chat_id in self.handlers.keys():
            try:
                if text[-1] == '?':
                    answer = 'Все вопросы вы сможете задать после заполнения всех данных, я отвечу на них как только смогу'
                else:
                    answer = self.handlers[chat_id].send(text)
                self.send_message(chat_id, user_id, answer)
            except StopIteration:
                del self.handlers[chat_id]
                self.names.append(chat_id)
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

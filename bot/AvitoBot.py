from requests import get, post
from time import sleep


class AvitoBot:
    def __init__(self, client_id, client_secret, work_base):
        self.client_id = client_id
        self.avitoapikey = None
        self.get_avito_key(client_id, client_secret)
        self.base = work_base

# TODO: Background scheduler for avitoapikey

    def get_avito_key(self, client_id, client_secret):
        self.avitoapikey = get(
            f'https://api.avito.ru/token/?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}').json()["access_token"]
        sleep(1)

    def get_webhooks(self):
        avitowebhook = 'https://api.avito.ru/messenger/v2/webhook'
        header = {'Authorization': 'Bearer ' + self.avitoapikey}
        payload = {'url': 'https://eazy-avito-bot.herokuapp.com/bot'}
        resp = post(avitowebhook, headers=header, json=payload)

    def send_message(self, chat_id, user_id, text):
        header = {'Authorization': 'Bearer ' + self.avitoapikey}
        payload = {"type": "text", "message": {"text": text}}
        ans = post(f"https://api.avito.ru/messenger/v1/accounts/{user_id}/chats/{chat_id}/messages", headers=header, json=payload)

    def message_handler(self, chat_id, user_id, text):
        with open('names.txt', 'r') as f:
            names = f.readlines()
            f.close()
        if chat_id not in names:
            names.append(chat_id + '\n')
            self.send_message(chat_id, user_id, 'text')
            with open('names.txt', 'w') as f:
                f.writelines(names)
        return 1

    def read_chat(self, chat_id, user_id):
        header = {'Authorization': 'Bearer ' + self.avitoapikey}
        post(f'https://api.avito.ru/messenger/v1/accounts/{user_id}/chats/{chat_id}/read', headers=header)

from requests import get, post
from time import sleep


class AvitoBot:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.avitoapikey = None
        self.get_avito_key()
        with open('names.txt', 'w') as f:
            for i in self.get_all_chats('169306001'):
                f.write(i['id'] + '\n')
            f.close()


    def get_avito_key(self):
        self.avitoapikey = get(
            f'https://api.avito.ru/token/?grant_type=client_credentials&client_id={self.client_id}&client_secret={self.client_secret}').json()[
            "access_token"]

    def get_webhooks(self):
        avitowebhook = 'https://api.avito.ru/messenger/v2/webhook'
        header = {'Authorization': 'Bearer ' + self.avitoapikey}
        payload = {'url': 'http://6b3b66dbc2ab.ngrok.io/bot'}
        resp = post(avitowebhook, headers=header, json=payload)

    def send_message(self, chat_id, user_id, text):
        header = {'Authorization': 'Bearer ' + self.avitoapikey}
        payload = {"type": "text", "message": {"text": text}}
        ans = post(f"https://api.avito.ru/messenger/v1/accounts/{user_id}/chats/{chat_id}/messages", headers=header,
                   json=payload)

    def message_handler(self, chat_id, user_id, text):
        with open('names.txt', 'r') as f:
            names = f.readlines()
            f.close()
        if chat_id + '\n' not in names:
            names.append(chat_id + '\n')
            self.send_message(chat_id, user_id, 'Здравствуйте')
            sleep(2)
            self.send_message(chat_id, user_id,
                              'Если Вы это не написали, укажите марку модель, год выпуска автомобиля и высоту проставок.')
            sleep(2)
            self.send_message(chat_id, user_id, 'Я чуть позже пришлю фото и цены')
            with open('names.txt', 'w') as f:
                f.writelines(names)
                f.close()
            self.read_chat(chat_id, user_id)
        return 1

    def read_chat(self, chat_id, user_id):
        header = {'Authorization': 'Bearer ' + self.avitoapikey}
        post(f'https://api.avito.ru/messenger/v1/accounts/{user_id}/chats/{chat_id}/read', headers=header)

    def get_all_chats(self, user_id):
        header = {'Authorization': 'Bearer ' + self.avitoapikey}
        chats = get(f'https://api.avito.ru/messenger/v1/accounts/{user_id}/chats', headers=header).json()['chats']
        return chats
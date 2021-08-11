from requests import post, get


class SdekBot:
    def __init__(self, sdek_client_id, sdek_client_secret, postal_from):
        self.sdek_client_id = sdek_client_id
        self.sdek_client_secret = sdek_client_secret
        self.postal_from = postal_from
        self.sdek_key = ''
        self.get_sdek_key()

    def get_sdek_key(self):
        params = {'grant_type': 'client_credentials', 'client_id': self.sdek_client_id,
                  'client_secret': self.sdek_client_secret}
        a = post('https://api.edu.cdek.ru/v2/oauth/token', params=params).json()
        self.sdek_key = 'Bearer ' + a['access_token']

    def get_sdek_price(self, address, city):
        header = {'Authorization': self.sdek_key}
        payload = {'tariff_code': 136, 'from_location': {'postal_code': self.postal_from},
                   'to_location': {'city': city, 'address': address}, 'packages': {'weight': 300}}
        try:
            resp = post('https://api.edu.cdek.ru/v2/calculator/tariff', headers=header, json=payload).json()['total_sum']
        except KeyError:
            resp = 0
        return resp

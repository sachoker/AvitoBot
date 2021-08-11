from bot.AvitoBot import AvitoBot
from apscheduler.schedulers.background import BackgroundScheduler
from openpyxl import load_workbook
from bot.SdekBot import SdekBot
import os

sched = BackgroundScheduler()
# client_id = "t7ivBRaOzMEhvubvwa4U"
# client_secret = "1xLUhklG6-FgIDWD0Zqb0YAt3tOXQgoEDZwR1YY_"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
base = load_workbook(fr"{ROOT_DIR}\База для бота.xlsx").active
client_id = '-iJiRUw8U1NukcfLAFzg'
client_secret = 'QRdEx3eJAWYrLvbloIZZNdQWqnDGrPi0fYNoqJyW'
sdek_client_id = 'EMscd6r9JnFiQ3bLoyjJY6eM78JrJceI'
sdek_client_secret = 'PjLZkKBHEiLK3YsjtNrt3TGNG0ahs3kG'
postal_from = '385000'
sdekbot = SdekBot(sdek_client_id, sdek_client_secret, postal_from)

from bot.dialog import dialog

bot = AvitoBot(client_id, client_secret, dialog, base)
bot.get_webhooks()
sched.add_job(bot.get_avito_key, 'interval', minutes=55)
sched.add_job(sdekbot.get_sdek_key, 'interval', minutes=55)

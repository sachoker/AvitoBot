from bot.AvitoBot import AvitoBot
from apscheduler.schedulers.background import BackgroundScheduler
from openpyxl import load_workbook

sched = BackgroundScheduler()
# client_id = "t7ivBRaOzMEhvubvwa4U"
# client_secret = "1xLUhklG6-FgIDWD0Zqb0YAt3tOXQgoEDZwR1YY_"
base = load_workbook(r"C:\Users\mv149\PycharmProjects\eazybot\bot\База для бота.xlsx").active
client_id = '-iJiRUw8U1NukcfLAFzg'
client_secret = 'QRdEx3eJAWYrLvbloIZZNdQWqnDGrPi0fYNoqJyW'

from dialog import dialog
bot = AvitoBot(client_id, client_secret, dialog, base)
bot.get_webhooks()
sched.add_job(bot.get_avito_key, 'interval', minutes=55)

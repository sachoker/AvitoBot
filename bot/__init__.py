from bot.AvitoBot import AvitoBot
from apscheduler.schedulers.background import BackgroundScheduler


sched = BackgroundScheduler()
client_id = "-iJiRUw8U1NukcfLAFzg"
client_secret = "QRdEx3eJAWYrLvbloIZZNdQWqnDGrPi0fYNoqJyW"

bot = AvitoBot(client_id, client_secret)
bot.get_webhooks()
sched.add_job(bot.get_avito_key, 'interval', minutes=55)


from flask import Flask
from AvitoBot import AvitoBot
from openpyxl import load_workbook

client_id = "-iJiRUw8U1NukcfLAFzg"
client_secret = "QRdEx3eJAWYrLvbloIZZNdQWqnDGrPi0fYNoqJyW"
app = Flask(__name__)
base = load_workbook("База для бота.xlsx").active

bot = AvitoBot(client_id, client_secret, base)
bot.get_webhooks()
import server

from env import TOKEN_API, BOT_WEBHOOK_URL
from aiogram import Bot, Dispatcher

flag = False
dependencies = {}
received_message = {
    'topic': '',
    'payload': ''
}

nto_bot = Bot(token=TOKEN_API)
nto_dp = Dispatcher(nto_bot)

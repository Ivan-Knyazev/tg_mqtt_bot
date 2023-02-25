from aiogram import Bot, Dispatcher
from app.env import TOKEN_API, BOT_WEBHOOK_URL
from app.mqtt import connect_mqtt

flag = False
dependencies = {}
received_message = {
    'topic': '',
    'payload': ''
}

nto_bot = Bot(token=TOKEN_API)
nto_dp = Dispatcher(nto_bot)

mqtt_client = connect_mqtt()
mqtt_client.loop_start()

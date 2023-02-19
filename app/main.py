import logging
from env import TOKEN_API, BOT_WEBHOOK_URL
from aiogram import Bot, Dispatcher, executor, types
from mqtt import mqtt_pub, mqtt_sub, mqtt_unsub

# from mqtt import mqtt

nto_bot = Bot(token=TOKEN_API)
nto_dp = Dispatcher(nto_bot)
HELP_COMMANDS = """
<b>Основные параметры</b>
/help - список команд
/start - начать работу с ботом
cat | pussy - получить кота

<b>Работа с MQTTT</b>
/pub &lt;topic&gt; &lt;message&gt; - отправить на topic
<em>(none) /sub &lt;topic&gt; &lt;message&gt; - подписаться на topic </em>
"""


async def on_startup(_):
    print('Bot is running')


@nto_dp.message_handler(commands=['start'])
async def hello(message: types.Message):
    # await message.reply("<em>Hello!<em>👋🏻\nIt's a NTO_MQTT_TEST_BOT :) 😎", parse_mode='HTML')
    await nto_bot.send_message(chat_id=message.from_user.id,
                               text="<b>Привет!</b>👋🏻\n"
                                    "Это <em>NTO_MQTT_TEST_BOT</em> :) 😎\n"
                                    "вы можете посмотреть команды с помощью /help",
                               parse_mode='HTML')


@nto_dp.message_handler(commands=['help', 'about'])
async def about(message: types.Message):
    await message.reply(HELP_COMMANDS, parse_mode='HTML')


@nto_dp.message_handler(regexp='(^cat[s]?$|puss)')
async def cat(message: types.Message):
    with open('../data/hello_cat.jpg', 'rb') as photo:
        await message.reply_photo(photo=photo, caption='Привет от котэ 😺')


@nto_dp.message_handler(commands=['pub'])
async def about(message: types.Message):
    # await mqtt.publish("/test", "Hello from Fastapi")
    data = message.text.split()
    if len(data) < 3:
        await message.reply('❌ не указан topic или message')
    else:
        msg = ' '.join(data[2:])
        mqtt_pub(topic=data[1], msg=msg)
        await message.reply('✅ ok')


@nto_dp.message_handler(commands=['sub'])
async def about(message: types.Message):
    # await mqtt.publish("/test", "Hello from Fastapi")
    data = message.text.split()
    if len(data) < 2:
        await message.reply('❌ не указан topic')
    else:
        mqtt_sub(topic=data[1])
        await message.reply("✅ ok\n"
                            "📨 подписка оформлена")


# @nto_dp.message_handler()
# async def echo(message: types.Message):
#     await nto_bot.send_message(chat_id=message.from_user.id,
#                                text=f"You said: '{message.text}'",
#                                parse_mode='HTML')


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    executor.start_polling(nto_dp, skip_updates=True, on_startup=on_startup)

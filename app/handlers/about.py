from aiogram import types, Dispatcher
import app.settings as sets

HELP_COMMANDS = """
<b>Основные параметры</b>
/help - список команд
/start - начать работу с ботом
<em>cat</em> - получить котэ

<b>Работа с MQTTT</b>
/pub &lt;topic&gt; <em>&lt;qos=0|1|2&gt;</em> &lt;payload&gt; - отправить на topic
• <em>qos</em> - опционально
/sub &lt;topic&gt; - подписаться на topic
/unsub &lt;topic&gt; - отменить подписку на topic
"""


# @nto_dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await sets.nto_bot.send_message(chat_id=message.from_user.id,
                                    text="<b>Привет!</b>👋🏻\n"
                                         "Это <em>NTO_MQTT_TEST_BOT</em> :) 😎\n"
                                         "Вы можете посмотреть команды с помощью /help",
                                    parse_mode='HTML')


# @nto_dp.message_handler(commands=['help', 'about', 'info'])
async def about(message: types.Message):
    await message.reply(HELP_COMMANDS, parse_mode='HTML')


def register_handlers_about(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(about, commands=['help', 'about', 'info'])

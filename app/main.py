import logging
import asyncio
from aiogram import executor, types

import settings as sets
from mqtt import mqtt_publish, mqtt_subscribe, mqtt_unsubscribe, connect_mqtt

# from paho.mqtt import client as client_mqtt
# from env import TOKEN_API, BOT_WEBHOOK_URL
# from env import MQTT_PORT, MQTT_HOST, MQTT_PASSWORD, MQTT_USERNAME, MQTT_CLIENT_ID


# DEPENDENCIES
# dependencies = sets.sets.dependencies
# sets.flag = sets.sets.flag
# sets.received_message = sets.sets.received_message

nto_bot = sets.nto_bot
nto_dp = sets.nto_dp


# TELEGRAM BOT

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

mqtt_client = connect_mqtt()
mqtt_client.loop_start()


async def on_startup(_):
    # print('Bot is running')
    asyncio.create_task(check())


@nto_dp.message_handler(commands=['start'])
async def hello(message: types.Message):
    # await sets.received_message.reply("<em>Hello!<em>👋🏻\nIt's a NTO_MQTT_TEST_BOT :) 😎", parse_mode='HTML')
    # global client
    # client = connect_mqtt()
    # client.loop_start()
    await nto_bot.send_message(chat_id=message.from_user.id,
                               text="<b>Привет!</b>👋🏻\n"
                                    "Это <em>NTO_MQTT_TEST_BOT</em> :) 😎\n"
                                    "Вы можете посмотреть команды с помощью /help",
                               parse_mode='HTML')


@nto_dp.message_handler(commands=['help', 'about', 'info'])
async def about(message: types.Message):
    await message.reply(HELP_COMMANDS, parse_mode='HTML')


@nto_dp.message_handler(regexp='(^cat[s]?$|puss)')
async def cat(message: types.Message):
    with open('../data/hello_cat.jpg', 'rb') as photo:
        await message.reply_photo(photo=photo, caption='Привет от котэ 😺')


@nto_dp.message_handler(commands=['pub'])
async def publish(message: types.Message):
    # await mqtt.publish("/test", "Hello from Fastapi")
    data = message.text.split()
    if len(data) < 3:
        await message.reply('❌ не указан topic или payload')
    else:
        global mqtt_client
        topic = data[1]
        success = '✅ ok\n' + '💾 опубликовано'
        if 'qos=' in data[2]:
            qos = int(data[2][4])
            msg = ' '.join(data[3:])
            if qos > 2:
                await message.reply('❌ qos может быть только 0, 1 или 2')
            else:
                mqtt_publish(client=mqtt_client, topic=topic, msg=msg, qos=qos)
                await message.reply(success)
        else:
            qos = 0
            msg = ' '.join(data[2:])
            mqtt_publish(client=mqtt_client, topic=topic, msg=msg, qos=qos)
            await message.reply(success)


@nto_dp.message_handler(commands=['sub'])
async def subscribe(message: types.Message):
    # await mqtt.publish("/test", "Hello from Fastapi")
    data = message.text.split()
    if len(data) < 2:
        await message.reply('❌ не указан topic')
    else:
        user_id = message.from_user.id
        topic = data[1]
        success = "✅ ok\n" + "📨 подписка оформлена"
        debug_message = '[DEBUG] ' + 'new subscriber: ' + str(user_id)

        global mqtt_client
        if topic in sets.dependencies:
            users = sets.dependencies[topic]
            if user_id not in users:
                users += [user_id]
                print(debug_message)
                await message.reply(success)
            else:
                await message.reply('❌ вы уже подписаны на данный topic')
        else:
            sets.dependencies[topic] = [user_id]
            mqtt_subscribe(client=mqtt_client, topic=topic)
            print(debug_message)
            await message.reply(success)


@nto_dp.message_handler(commands=['unsub'])
async def unsubscribe(message: types.Message):
    data = message.text.split()
    if len(data) < 2:
        await message.reply('❌ не указан topic')
    else:
        # global user_id
        user_id = message.from_user.id
        topic = data[1]
        error = '❌ вы не подписаны на данный topic'

        global mqtt_client
        if topic in sets.dependencies:
            users = sets.dependencies[topic]
            if user_id in users:
                users.remove(user_id)
                print('[DEBUG] ' + 'unsubscribe: ' + str(user_id))
                await message.reply("✅ ok\n"
                                    "📤 подписка отменена")
            else:
                await message.reply(error)
            if len(users) == 0:
                mqtt_unsubscribe(client=mqtt_client, topic=topic)
                sets.dependencies.pop(topic)
        else:
            await message.reply(error)


async def check():
    # global sets.flag, sets.received_message
    print('Start Check task')
    # if not sets.flag:
    #     await asyncio.sleep(5)
    while True:
        if sets.flag:
            topic = sets.received_message['topic']
            payload = sets.received_message['payload']
            if topic in sets.dependencies:
                if len(topic) > 0:
                    for user_id in sets.dependencies[topic]:
                        text = f"🔹 <em>From <b>{topic}</b></em> \n" \
                               f"{payload}"
                        await nto_bot.send_message(chat_id=user_id, text=text, parse_mode='HTML')
                else:
                    print('[ERROR] ' + 'Nobody has subscribed to this topic!')
            else:
                print('[ERROR] ' + 'This topic is not in the `sets.dependencies`!')
            print('[DEBUG] ' + 'sets.dependencies: ', sets.dependencies)
            sets.flag = False
        else:
            await asyncio.sleep(1)


# @nto_dp.message_handler()
# async def echo(sets.received_message: types.Message):
#     await nto_bot.send_message(chat_id=sets.received_message.from_user.id,
#                                text=f"You said: '{sets.received_message.text}'",
#                                parse_mode='HTML')

# async def main():
#     task_1 = asyncio.create_task(executor.start_polling(nto_dp, skip_updates=True, on_startup=on_startup))
#     task_2 = asyncio.create_task(check())
#     await asyncio.gather(task_2, task_1)

if __name__ == '__main__':
    # asyncio.run(main())

    logging.basicConfig(level=logging.INFO)
    # ioloop = asyncio.new_event_loop()
    # # tasks = [ioloop.create_task(check()),
    # #          ioloop.create_task(executor.start_polling(nto_dp, skip_updates=True, on_startup=on_startup))]
    # # wait_tasks = asyncio.wait(tasks)
    # # ioloop.run_until_complete(wait_tasks)
    # asyncio.run(main(ioloop))

    # asyncio.create_task(executor.start_polling(nto_dp, skip_updates=True, on_startup=on_startup))
    # asyncio.create_task(main())

    executor.start_polling(nto_dp, skip_updates=True, on_startup=on_startup)
    # asyncio.run(echo())

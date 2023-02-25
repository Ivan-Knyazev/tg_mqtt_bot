from aiogram import types, Dispatcher
import app.settings as sets
from app.mqtt import mqtt_publish, mqtt_subscribe, mqtt_unsubscribe


# @nto_dp.message_handler(commands=['pub'])
async def publish(message: types.Message):
    # await mqtt.publish("/test", "Hello from Fastapi")
    data = message.text.split()
    if len(data) < 3:
        await message.reply('❌ не указан topic или payload')
    else:
        topic = data[1]
        success = '✅ ok\n' + '💾 опубликовано'
        if 'qos=' in data[2]:
            qos = int(data[2][4])
            msg = ' '.join(data[3:])
            if qos > 2:
                await message.reply('❌ qos может быть только 0, 1 или 2')
            else:
                mqtt_publish(client=sets.mqtt_client, topic=topic, msg=msg, qos=qos)
                await message.reply(success)
        else:
            qos = 0
            msg = ' '.join(data[2:])
            mqtt_publish(client=sets.mqtt_client, topic=topic, msg=msg, qos=qos)
            await message.reply(success)


# @nto_dp.message_handler(commands=['sub'])
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
            mqtt_subscribe(client=sets.mqtt_client, topic=topic)
            print(debug_message)
            await message.reply(success)


# @nto_dp.message_handler(commands=['unsub'])
async def unsubscribe(message: types.Message):
    data = message.text.split()
    if len(data) < 2:
        await message.reply('❌ не указан topic')
    else:
        # global user_id
        user_id = message.from_user.id
        topic = data[1]
        error = '❌ вы не подписаны на данный topic'

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
                mqtt_unsubscribe(client=sets.mqtt_client, topic=topic)
                sets.dependencies.pop(topic)
        else:
            await message.reply(error)


def register_handlers_mqtt(dp: Dispatcher):
    dp.register_message_handler(publish, commands=['pub'])
    dp.register_message_handler(subscribe, commands=['sub'])
    dp.register_message_handler(unsubscribe, commands=['unsub'])

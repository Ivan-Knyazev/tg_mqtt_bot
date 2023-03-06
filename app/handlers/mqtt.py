from aiogram import types, Dispatcher
import app.settings as sets
from app.mqtt import mqtt_publish, mqtt_subscribe, mqtt_unsubscribe
from app.models.base import async_session
from app.utils.base_operations import get_users_by_topic
from app.services import topics


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
    data = message.text.split()
    if len(data) < 2:
        await message.reply('❌ не указан topic')
    else:
        user_id = message.from_user.id
        topic = data[1]
        success = "✅ ok\n" + "📨 подписка оформлена"
        debug_message = '[DEBUG] ' + 'new subscriber ' + str(user_id) + ' for topic ' + topic

        users_from_topic = await get_users_by_topic(topic)

        async with async_session() as session:
            async with session.begin():
                if user_id not in users_from_topic:

                    if len(users_from_topic) == 0:
                        mqtt_subscribe(client=sets.mqtt_client, topic=topic)
                        print(f'[DEBUG] New MQTT Subscribe to {topic} from {user_id}')

                    topics.create_topic(session, topic, user_id)
                    try:
                        await session.commit()
                        print(debug_message)
                        await message.reply(success)
                    except:
                        await session.rollback()
                        print(f'[ERROR] Topic `{topic}` for user `{user_id}` has not been added to the database!')
                        await message.reply('❌ ERROR ... fixing ...')
                else:
                    await message.reply('❌ вы уже подписаны на данный topic')


# @nto_dp.message_handler(commands=['unsub'])
async def unsubscribe(message: types.Message):
    data = message.text.split()
    if len(data) < 2:
        await message.reply('❌ не указан topic')
    else:
        user_id = message.from_user.id
        topic = data[1]
        error = '❌ ERROR ... fixing ...'
        status = False

        async with async_session() as session:
            async with session.begin():
                result = await topics.check_topic(session, user_id, topic)
                if result['status_code'] == 0:
                    print('[ERROR] 2 entries in the database for one topic and a user!')
                    await message.reply(error)
                elif result['status_code'] == 1:
                    await message.reply('❌ вы не подписаны на данный topic')
                else:
                    status = True
        if status:
            async with async_session() as session:
                async with session.begin():
                    await topics.delete_topic(session, user_id, topic)
                    try:
                        await session.commit()
                        print('[DEBUG] ' + 'unsubscribe ' + str(user_id) + ' from topic ' + topic)
                        await message.reply("✅ ok\n"
                                            "📤 подписка отменена")
                    except:
                        await session.rollback()
                        print(f'[ERROR] Topic `{topic}` for user `{user_id}` has not been deleted from the database!')
                        await message.reply(error)

        users_from_topic = await get_users_by_topic(topic)
        if len(users_from_topic) == 0:
            mqtt_unsubscribe(client=sets.mqtt_client, topic=topic)


def register_handlers_mqtt(dp: Dispatcher):
    dp.register_message_handler(publish, commands=['pub'])
    dp.register_message_handler(subscribe, commands=['sub'])
    dp.register_message_handler(unsubscribe, commands=['unsub'])

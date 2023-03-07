import asyncio
import app.settings as sets
from app.utils.base_operations import get_users_by_topic


async def check():
    print('Start Check task')
    # await asyncio.sleep(15)
    while True:
        if sets.flag:
            topic = sets.received_message['topic']
            payload = sets.received_message['payload']

            users = await get_users_by_topic(topic)
            if len(users) == 0:
                print('[ERROR] ' + 'Nobody has subscribed to this topic!')
            else:
                for user_id in users:
                    text = f"🔹 <em>From <b>{topic}</b></em> \n" \
                           f"{payload}"
                    await sets.nto_bot.send_message(chat_id=user_id, text=text, parse_mode='HTML')
            sets.flag = False
        else:
            await asyncio.sleep(0.5)

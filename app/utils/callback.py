import asyncio
import app.settings as sets


async def check():
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
                        await sets.nto_bot.send_message(chat_id=user_id, text=text, parse_mode='HTML')
                else:
                    print('[ERROR] ' + 'Nobody has subscribed to this topic!')
            else:
                print('[ERROR] ' + 'This topic is not in the `sets.dependencies`!')
            print('[DEBUG] ' + 'sets.dependencies: ', sets.dependencies)
            sets.flag = False
        else:
            await asyncio.sleep(1)

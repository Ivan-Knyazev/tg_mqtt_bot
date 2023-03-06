import app.settings as sets
from app.mqtt import mqtt_subscribe
from app.models.base import async_session
from app.services import topics


async def get_users_by_topic(topic: str) -> list:
    async with async_session() as session:
        async with session.begin():
            users_from_topic = await topics.get_users(session, topic)
            # topics_from_user = await topics.get_topics_by_user_id(session, user_id)

            return users_from_topic


async def sub_all_topics():
    async with async_session() as session:
        async with session.begin():
            all_topics = await topics.get_topics(session)
            set_topics = list(set(all_topics))
            # print(set_topics)
    for topic in set_topics:
        mqtt_subscribe(client=sets.mqtt_client, topic=topic)
    print('Subscribing on all topics')

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Topic


async def check_topic(
        session: AsyncSession,
        user_id: int,
        topic: str
) -> dict:
    result = await session.execute(select(Topic).where(
        Topic.user_id == user_id).where(
        Topic.topic == topic))
    data = result.fetchall()
    if len(data) > 1:
        print(data)
        return {'status_code': 0}
    elif len(data) == 0:
        return {'status_code': 1}
    else:
        return {'status_code': 2}


def create_topic(
        session: AsyncSession,
        topic: str,
        user_id: int
) -> dict:
    new_topic = Topic(
        topic=topic,
        user_id=user_id
    )
    session.add(new_topic)
    return {'id': new_topic.user_id, 'topic': new_topic.topic}


async def delete_topic(
        session: AsyncSession,
        user_id: int,
        topic: str
) -> dict:
    query = delete(Topic).where(
        Topic.user_id == user_id).where(
        Topic.topic == topic)
    query.execution_options(synchronize_session="fetch")
    await session.execute(query)

    # result = await session.execute(select(Topic).where(
    #     Topic.user_id == user_id).where(
    #     Topic.topic == topic))
    # res = result.one()
    # await session.delete(res)

    return {'id': user_id, 'topic': topic}


async def get_users(
        session: AsyncSession,
        topic: str
) -> list:
    # topics = await session.query(Topic).filter_by(user_id=user_id).all()
    result = await session.execute(select(Topic).where(Topic.topic == topic))
    users = []
    for user in result.fetchall():
        iterator = user[0].__dict__
        users += [iterator['user_id']]
    return users


async def get_topics(
        session: AsyncSession,
) -> list:
    result = await session.execute(select(Topic).order_by(Topic.topic_id))
    topics = []
    for topic in result.fetchall():
        iterator = topic[0].__dict__
        topics += [iterator['topic']]
    return topics

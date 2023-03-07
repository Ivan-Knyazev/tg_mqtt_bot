from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import User


def create_user(
        session: AsyncSession,
        username: str,
        telegram_id: int,
        is_admin: bool
) -> dict:
    new_user = User(
        username=username,
        telegram_id=telegram_id,
        is_admin=is_admin
    )
    session.add(new_user)
    # session.flush()
    return {'id': new_user.telegram_id, 'username': new_user.username}


async def get_user_by_id(
        session: AsyncSession,
        user_id: int
):
    # user = await session.get(User, user_id)
    # user = await session.query(User).filter_by(telegram_id=user_id).first()
    user = await session.execute(select(User).where(User.telegram_id == user_id))
    return user

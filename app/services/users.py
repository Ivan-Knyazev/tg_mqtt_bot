from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import User

async def create_user(
        session: AsyncSession,
        username:str,
        telegram_id: int,
        is_admin: bool
):
    new_user = User(
        username=username,

    )

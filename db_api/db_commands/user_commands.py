from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from db_api.database import get_session
from db_api.tables.user_table import Users


async def add_user(telegram_id: int, tg_username: str, referral_id: str, notification_upper_limit: float, language: str):
    async with get_session() as session:
        user = Users(
            telegram_id=telegram_id,
            tg_username=tg_username,
            referral_id = referral_id,
            notification_upper_limit=notification_upper_limit,
            language=language
        )
        session.add(user)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()


async def select_user(telegram_id: int):
    async with get_session() as session:
        sql = select(Users).where(Users.telegram_id == telegram_id)
        user = await session.execute(sql)
        return user.scalar()


async def read_users():
    async with get_session() as session:
        sql = select(Users)
        t_hash = await session.execute(sql)
        return t_hash.scalars()


async def add_upper_limit(telegram_id, gas_price):
    async with get_session() as session:
        sql = update(Users).where(Users.telegram_id == telegram_id).values(notification_upper_limit=gas_price)
        await session.execute(sql)
        await session.commit()

async def set_user_language(telegram_id, language):
    async with get_session() as session:
        sql = update(Users).where(Users.telegram_id == telegram_id).values(language=language)
        await session.execute(sql)
        await session.commit()

async def get_limit(telegram_id: int):
    async with get_session() as session:
        sql = select(Users.notification_upper_limit).where(Users.telegram_id == telegram_id)
        user = await session.execute(sql)
        return user.scalar()

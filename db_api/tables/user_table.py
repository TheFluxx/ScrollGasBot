from datetime import datetime

from sqlalchemy import Column, Integer, String, BigInteger, Boolean, Float, DateTime

from db_api.database import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True)
    tg_username = Column(String)
    is_referral = Column(Boolean, default=False)
    referral_id = Column(String)
    notification_upper_limit = Column(Float)
    language = Column(String)

from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Boolean, String, TIMESTAMP, ForeignKey, BigInteger

Base = declarative_base()


class User(Base):
    """ users using the bot """
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(50))
    telegram_id = Column(BigInteger, nullable=False, unique=True)
    is_admin = Column(Boolean, default=False)
    start_usage = Column(TIMESTAMP, default=datetime.utcnow)


class Topic(Base):
    """ Topics and users subscribed to them """
    __tablename__ = 'topics'

    topic_id = Column(Integer, autoincrement=True, primary_key=True)
    topic = Column(String(50), nullable=False)
    user_id = Column(ForeignKey('users.telegram_id'))
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)

# metadata = MetaData()
#
# User = Table(
#     "users",
#     metadata,
#     Column("id", Integer, autoincrement=True, primary_key=True),
#     Column("username", String(50), unique=True),
#     Column("telegram_id", Integer, nullable=False, unique=True),
#     Column("is_admin", Boolean, default=False),
#     Column("start_usage", TIMESTAMP, default=datetime.utcnow)
# )
#
# Topic = Table(
#     "topics",
#     metadata,
#     Column("topic_id", Integer, autoincrement=True, primary_key=True),
#     Column("topic", String(50), nullable=False),
#     Column("user_id", ForeignKey('users.id')),
#     Column("timestamp", TIMESTAMP, default=datetime.utcnow)
# )

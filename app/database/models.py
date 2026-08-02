from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, nullable=False)

    email = Column(String, unique=True, nullable=False)

    password = Column(String, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    chats = relationship(
        "ChatSession",
        back_populates="user",
        cascade="all, delete"
    )


class ChatSession(Base):

    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(
        String,
        default="New Chat"
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="chats"
    )

    messages = relationship(
        "Message",
        back_populates="chat",
        cascade="all, delete"
    )


class Message(Base):

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    chat_id = Column(
        Integer,
        ForeignKey("chat_sessions.id")
    )

    role = Column(String)

    content = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    chat = relationship(
        "ChatSession",
        back_populates="messages"
    )
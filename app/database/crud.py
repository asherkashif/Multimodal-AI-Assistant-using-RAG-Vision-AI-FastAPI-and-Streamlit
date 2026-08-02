from sqlalchemy.orm import Session

from .models import (
    User,
    ChatSession,
    Message
)


# ==========================
# Chat Session
# ==========================

def create_chat(
    db: Session,
    user_id: int,
    title="New Chat"
):
    chat = ChatSession(
        user_id=user_id,
        title=title
    )

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat


# ==========================
# Messages
# ==========================

def save_message(
    db: Session,
    chat_id: int,
    role: str,
    content: str
):
    message = Message(
        chat_id=chat_id,
        role=role,
        content=content
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def get_messages(
    db: Session,
    chat_id: int
):
    return (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.id)
        .all()
    )
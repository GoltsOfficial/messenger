from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


chat_user = Table(
    "chat_user",
    Base.metadata,
    Column(
        "chat_id",
        Integer,
        ForeignKey("chat.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "user_id",
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    chats: Mapped[list["Chat"]] = relationship(
        secondary=chat_user,
        back_populates="users",
    )
    messages: Mapped[list["Message"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )


class Chat(Base):
    __tablename__ = "chat"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    users: Mapped[list[User]] = relationship(
        secondary=chat_user,
        back_populates="chats",
    )
    messages: Mapped[list["Message"]] = relationship(
        back_populates="chat",
        cascade="all, delete-orphan",
        order_by="Message.created_at",
    )


class Message(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("chat.id", ondelete="CASCADE"), index=True
    )
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), index=True
    )
    text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    chat: Mapped["Chat"] = relationship(back_populates="messages")
    author: Mapped["User"] = relationship(back_populates="messages")

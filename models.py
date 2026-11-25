from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[String] = mapped_column(String, unique=True)
    created_at: Mapped[DateTime] = mapped_column(server_default=func.now())


class Chat(Base):
    __tablename__ = "chat"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[String] = mapped_column(String(100), unique=True, index=True)
    created_at: Mapped[DateTime] = mapped_column(server_default=func.now())

from sqlalchemy.orm import Session
import models


class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, chat_id: int, author_id: int, text: str) -> models.Message:
        msg = models.Message(chat_id=chat_id, author_id=author_id, text=text)
        self.db.add(msg)
        self.db.commit()
        self.db.refresh(msg)
        return msg

    def list_by_chat(self, chat_id: int, limit: int = 50) -> list[models.Message]:
        return (
            self.db.query(models.Message)
            .filter(models.Message.chat_id == chat_id)
            .order_by(models.Message.created_at)
            .limit(limit)
            .all()
        )

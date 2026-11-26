from sqlalchemy.orm import Session
import models


class ChatRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, users: list[models.User]) -> models.Chat:
        chat = models.Chat(name=name, users=users)
        self.db.add(chat)
        self.db.commit()
        self.db.refresh(chat)
        return chat

    def get_by_id(self, chat_id: int) -> models.Chat | None:
        return self.db.get(models.Chat, chat_id)

    def list_for_user(self, user_id: int) -> list[models.Chat]:
        return (
            self.db.query(models.Chat)
            .join(models.Chat.users)
            .filter(models.User.id == user_id)
            .all()
        )

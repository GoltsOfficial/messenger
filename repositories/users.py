from sqlalchemy.orm import Session
import models


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> models.User | None:
        return self.db.get(models.User, user_id)

    def get_by_username(self, username: str) -> models.User | None:
        return (
            self.db.query(models.User)
            .filter(models.User.username == username)
            .first()
        )

    def create(self, username: str) -> models.User:
        user = models.User(username=username)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

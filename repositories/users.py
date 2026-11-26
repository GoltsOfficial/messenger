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

    def list_all(self) -> list[models.User]:
        return self.db.query(models.User).order_by(models.User.username).all()

    def create(self, username: str, password_hash: str) -> models.User:
        user = models.User(username=username, password_hash=password_hash)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

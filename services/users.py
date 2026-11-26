from fastapi import HTTPException
from repositories.users import UserRepository
from schemas import UserCreate


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create(self, payload: UserCreate):
        if self.repo.get_by_username(payload.username) is not None:
            raise HTTPException(status_code=409, detail="Username already taken")
        return self.repo.create(payload.username)
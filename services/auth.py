from fastapi import HTTPException

from repositories.users import UserRepository
from schemas import UserCreate
from security import hash_password, verify_password, create_access_token


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register(self, payload: UserCreate):
        if self.repo.get_by_username(payload.username) is not None:
            raise HTTPException(status_code=409, detail="Username already taken")
        return self.repo.create(
            username=payload.username,
            password_hash=hash_password(payload.password),
        )

    def authenticate(self, username: str, password: str):
        user = self.repo.get_by_username(username)
        if user is None or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {
            "access_token": create_access_token(user.id),
            "token_type": "bearer",
        }

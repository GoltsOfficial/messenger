from fastapi import HTTPException
from repositories.chats import ChatRepository
from repositories.users import UserRepository
from schemas import ChatCreate


class ChatService:
    def __init__(self, chat_repo: ChatRepository, user_repo: UserRepository):
        self.chat_repo = chat_repo
        self.user_repo = user_repo

    def create(self, payload: ChatCreate):
        users = []
        for uid in payload.user_ids:
            user = self.user_repo.get_by_id(uid)
            if user is None:
                raise HTTPException(status_code=404, detail=f"User {uid} not found")
            users.append(user)
        return self.chat_repo.create(name=payload.name, users=users)

    def list_for_user(self, user_id: int):
        if self.user_repo.get_by_id(user_id) is None:
            raise HTTPException(status_code=404, detail="User not found")
        return self.chat_repo.list_for_user(user_id)

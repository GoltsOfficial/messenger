from fastapi import HTTPException
from repositories.messages import MessageRepository
from repositories.chats import ChatRepository
from repositories.users import UserRepository
from schemas import MessageCreate


class MessageService:
    def __init__(
            self,
            message_repo: MessageRepository,
            chat_repo: ChatRepository,
            user_repo: UserRepository,
    ):
        self.message_repo = message_repo
        self.chat_repo = chat_repo
        self.user_repo = user_repo

    def send(self, chat_id: int, payload: MessageCreate):
        chat = self.chat_repo.get_by_id(chat_id)
        if chat is None:
            raise HTTPException(status_code=404, detail="Chat not found")
        if self.user_repo.get_by_id(payload.author_id) is None:
            raise HTTPException(status_code=404, detail="Author not found")
        return self.message_repo.create(
            chat_id=chat_id,
            author_id=payload.author_id,
            text=payload.text,
        )

    def list_by_chat(self, chat_id: int, limit: int = 50):
        if self.chat_repo.get_by_id(chat_id) is None:
            raise HTTPException(status_code=404, detail="Chat not found")
        return self.message_repo.list_by_chat(chat_id, limit)

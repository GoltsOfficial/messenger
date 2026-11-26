from fastapi import HTTPException

from repositories.messages import MessageRepository
from repositories.chats import ChatRepository
from schemas import MessageCreate


class MessageService:
    def __init__(
            self,
            message_repo: MessageRepository,
            chat_repo: ChatRepository,
    ):
        self.message_repo = message_repo
        self.chat_repo = chat_repo

    def _ensure_member(self, chat_id: int, user_id: int):
        chat = self.chat_repo.get_by_id(chat_id)
        if chat is None:
            raise HTTPException(status_code=404, detail="Chat not found")
        if not any(u.id == user_id for u in chat.users):
            raise HTTPException(status_code=403, detail="Not a member of this chat")
        return chat

    def send(self, chat_id: int, payload: MessageCreate, author_id: int):
        self._ensure_member(chat_id, author_id)
        return self.message_repo.create(
            chat_id=chat_id,
            author_id=author_id,
            text=payload.text,
        )

    def list_by_chat(self, chat_id: int, user_id: int, limit: int = 50):
        self._ensure_member(chat_id, user_id)
        return self.message_repo.list_by_chat(chat_id, limit)

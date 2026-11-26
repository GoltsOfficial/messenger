from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from repositories.messages import MessageRepository
from repositories.chats import ChatRepository
from repositories.users import UserRepository
from schemas import MessageCreate, MessageOut
from services.messages import MessageService

router = APIRouter(prefix="/chats", tags=["messages"])


def get_message_service(db: Session = Depends(get_db)) -> MessageService:
    return MessageService(
        MessageRepository(db),
        ChatRepository(db),
        UserRepository(db),
    )


@router.post("/{chat_id}/messages", response_model=MessageOut, status_code=201)
def send_message(
        chat_id: int,
        payload: MessageCreate,
        service: MessageService = Depends(get_message_service),
):
    return service.send(chat_id, payload)


@router.get("/{chat_id}/messages", response_model=list[MessageOut])
def list_messages(
        chat_id: int,
        limit: int = 50,
        service: MessageService = Depends(get_message_service),
):
    return service.list_by_chat(chat_id, limit)

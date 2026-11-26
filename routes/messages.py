from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models
from database import get_db
from dependencies import get_current_user
from repositories.messages import MessageRepository
from repositories.chats import ChatRepository
from schemas import MessageCreate, MessageOut
from services.messages import MessageService

router = APIRouter(prefix="/chats", tags=["messages"])


def get_message_service(db: Session = Depends(get_db)) -> MessageService:
    return MessageService(
        MessageRepository(db),
        ChatRepository(db),
    )


@router.post("/{chat_id}/messages", response_model=MessageOut, status_code=201)
def send_message(
        chat_id: int,
        payload: MessageCreate,
        service: MessageService = Depends(get_message_service),
        current_user: models.User = Depends(get_current_user),
):
    return service.send(chat_id, payload, current_user.id)


@router.get("/{chat_id}/messages", response_model=list[MessageOut])
def list_messages(
        chat_id: int,
        limit: int = 50,
        service: MessageService = Depends(get_message_service),
        current_user: models.User = Depends(get_current_user),
):
    return service.list_by_chat(chat_id, current_user.id, limit)

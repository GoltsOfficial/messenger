from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models
from database import get_db
from dependencies import get_current_user
from repositories.chats import ChatRepository
from repositories.users import UserRepository
from schemas import ChatCreate, ChatOut
from services.chats import ChatService

router = APIRouter(prefix="/chats", tags=["chats"])


def get_chat_service(db: Session = Depends(get_db)) -> ChatService:
    return ChatService(ChatRepository(db), UserRepository(db))


@router.post("", response_model=ChatOut, status_code=201)
def create_chat(
        payload: ChatCreate,
        service: ChatService = Depends(get_chat_service),
        current_user: models.User = Depends(get_current_user),
):
    return service.create(payload, current_user.id)


@router.get("", response_model=list[ChatOut])
def list_my_chats(
        service: ChatService = Depends(get_chat_service),
        current_user: models.User = Depends(get_current_user),
):
    return service.list_for_user(current_user.id)

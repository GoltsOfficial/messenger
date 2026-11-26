from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
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
):
    return service.create(payload)


@router.get("/user/{user_id}", response_model=list[ChatOut])
def list_user_chats(
        user_id: int,
        service: ChatService = Depends(get_chat_service),
):
    return service.list_for_user(user_id)

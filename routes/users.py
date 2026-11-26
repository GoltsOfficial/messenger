from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models
from database import get_db
from dependencies import get_current_user
from repositories.users import UserRepository
from schemas import UserOut
from services.users import UserService

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))


@router.get("", response_model=list[UserOut])
def list_users(
        service: UserService = Depends(get_user_service),
        current_user: models.User = Depends(get_current_user),
):
    return service.list_all()


@router.get("/me", response_model=UserOut)
def me(current_user: models.User = Depends(get_current_user)):
    return current_user

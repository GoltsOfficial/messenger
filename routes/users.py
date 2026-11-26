from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from repositories.users import UserRepository
from schemas import UserCreate, UserOut
from services.users import UserService

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))


@router.post("", response_model=UserOut, status_code=201)
def create_user(
        payload: UserCreate,
        service: UserService = Depends(get_user_service),
):
    return service.create(payload)

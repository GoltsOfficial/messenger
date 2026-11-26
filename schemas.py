from datetime import datetime
from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=100)


class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    user_ids: list[int] = Field(min_length=1)


class ChatOut(BaseModel):
    id: int
    name: str
    created_at: datetime

    model_config = {"from_attributes": True}


class MessageCreate(BaseModel):
    author_id: int
    text: str = Field(min_length=1, max_length=250)


class MessageOut(BaseModel):
    id: int
    chat_id: int
    author_id: int
    text: str
    created_at: datetime

    model_config = {"from_attributes": True}

from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: str

    @field_validator("password")
    @classmethod
    def password_fits_bcrypt(cls, value: str) -> str:
        # bcrypt учитывает не больше 72 байт пароля
        if len(value.encode()) > 72:
            raise ValueError("Password is longer than 72 bytes")
        return value


class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ChatCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    user_ids: list[int] = Field(default_factory=list)


class ChatOut(BaseModel):
    id: int
    name: str
    created_at: datetime

    model_config = {"from_attributes": True}


class MessageCreate(BaseModel):
    text: str = Field(min_length=1, max_length=250)


class MessageOut(BaseModel):
    id: int
    chat_id: int
    author_id: int
    text: str
    created_at: datetime

    model_config = {"from_attributes": True}

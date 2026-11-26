from fastapi import FastAPI

from routes import users, chats, messages

app = FastAPI(title="Messenger")

app.include_router(users.router)
app.include_router(chats.router)
app.include_router(messages.router)

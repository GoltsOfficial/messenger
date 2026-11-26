# Messenger

Backend + простой веб-интерфейс мессенджера: пользователи, JWT-авторизация, чаты и сообщения.

## Возможности

- Регистрация и вход (JWT / OAuth2 password flow)
- Создание чатов с участниками
- Список своих чатов
- Отправка и просмотр сообщений
- Веб-UI: вход, список чатов, переписка

## Стек

| Компонент | Технология |
|-----------|------------|
| API | FastAPI |
| Auth | JWT (python-jose), bcrypt, OAuth2PasswordBearer |
| ORM | SQLAlchemy 2.x |
| БД | PostgreSQL 16 |
| Миграции | Alembic |
| Валидация | Pydantic v2 |
| Сервер | Uvicorn |
| Фронтенд | HTML / CSS / JS (static) |
| Контейнеры | Docker, Docker Compose |

Архитектура API: **routes → services → repositories**.

## Быстрый старт (Docker)

В корне репозитория, ветка `dev`:

```bash
cp .env.example .env
# при необходимости отредактируй SECRET_KEY

docker compose up --build
```

После запуска:

- Веб-интерфейс: [http://localhost:9000](http://localhost:9000)
- Swagger UI: [http://localhost:9000/docs](http://localhost:9000/docs)
- ReDoc: [http://localhost:9000/redoc](http://localhost:9000/redoc)

Миграции Alembic применяются автоматически при старте контейнера.

## Переменные окружения

```env
DATABASE_URL=postgresql+psycopg://messenger:messenger@postgres:5432/messenger
SECRET_KEY=replace-with-random-32-bytes-token
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Tests
TEST_DATABASE_URL=postgresql+psycopg://messenger:messenger@localhost:5432/messenger_test
```

## API

### Auth

| Метод | Путь | Описание |
|-------|------|----------|
| `POST` | `/auth/register` | Регистрация (`username`, `password`) JSON |
| `POST` | `/auth/login` | Вход (form: `username`, `password`) → JWT |

### Пользователи (Bearer token)

| Метод | Путь | Описание |
|-------|------|----------|
| `GET` | `/users/me` | Текущий пользователь |
| `GET` | `/users` | Список пользователей |

### Чаты и сообщения (Bearer token)

| Метод | Путь | Описание |
|-------|------|----------|
| `POST` | `/chats` | Создать чат (`name`, `user_ids`) |
| `GET` | `/chats` | Мои чаты |
| `POST` | `/chats/{id}/messages` | Отправить сообщение (`text`) |
| `GET` | `/chats/{id}/messages` | История (`limit`) |

## Локальный запуск без Docker

```bash
pip install -r requirements.txt
cp .env.example .env
# DATABASE_URL на localhost

alembic upgrade head
uvicorn main:app --reload --host 0.0.0.0 --port 9000
```

## Структура проекта

```
.
├── alembic/
├── repositories/
├── routes/               # auth, users, chats, messages
├── services/
├── static/               # веб-UI
│   ├── css/
│   ├── js/
│   └── index.html
├── config.py
├── database.py
├── dependencies.py       # get_current_user (JWT)
├── main.py
├── models.py
├── schemas.py
├── security.py           # bcrypt + JWT
├── Dockerfile
├── docker-compose.yaml
└── .env.example
```

## Требования

- Docker и Docker Compose (рекомендуется)
- либо Python 3.12+ и PostgreSQL 16

# Messenger

Backend API для простого мессенджера: пользователи, чаты и сообщения.

## Возможности

- Создание пользователей
- Создание чатов с участниками
- Список чатов пользователя
- Отправка сообщений в чат
- Получение истории сообщений чата

## Стек

| Компонент | Технология |
|-----------|------------|
| API | FastAPI |
| ORM | SQLAlchemy 2.x |
| БД | PostgreSQL 16 |
| Миграции | Alembic |
| Валидация | Pydantic v2 |
| Сервер | Uvicorn |
| Контейнеры | Docker, Docker Compose |

Архитектура: **routes → services → repositories**.

## Быстрый старт (Docker)

В корне репозитория, ветка `dev`:

```bash
cp .env.example .env
# при необходимости отредактируй SECRET_KEY

docker compose up --build
```

После запуска:

- API: [http://localhost:9000](http://localhost:9000)
- Swagger UI: [http://localhost:9000/docs](http://localhost:9000/docs)
- ReDoc: [http://localhost:9000/redoc](http://localhost:9000/redoc)

Миграции Alembic применяются автоматически при старте контейнера.

## Переменные окружения

Скопируй `.env.example` в `.env` и при необходимости измени значения:

```env
DATABASE_URL=postgresql+psycopg://messenger:messenger@postgres:5432/messenger
SECRET_KEY=replace-with-random-32-bytes-token
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Tests
TEST_DATABASE_URL=postgresql+psycopg://messenger:messenger@localhost:5432/messenger_test
```

В `docker-compose.yaml` `DATABASE_URL` уже задан для контейнера приложения. `SECRET_KEY` обязателен (читается из `.env`).

## Основные эндпоинты

### Пользователи

| Метод | Путь | Описание |
|-------|------|----------|
| `POST` | `/users` | Создать пользователя (`username`) |

### Чаты

| Метод | Путь | Описание |
|-------|------|----------|
| `POST` | `/chats` | Создать чат (`name`, `user_ids`) |
| `GET` | `/chats/user/{user_id}` | Список чатов пользователя |

### Сообщения

| Метод | Путь | Описание |
|-------|------|----------|
| `POST` | `/chats/{chat_id}/messages` | Отправить сообщение (`author_id`, `text`) |
| `GET` | `/chats/{chat_id}/messages` | История сообщений (`limit`, по умолчанию 50) |

## Локальный запуск без Docker

1. Подними PostgreSQL и создай БД `messenger`.
2. Установи зависимости:

```bash
pip install -r requirements.txt
```

3. Создай `.env` (для локальной БД укажи `localhost` в `DATABASE_URL`).
4. Примени миграции и запусти API:

```bash
alembic upgrade head
uvicorn main:app --reload --host 0.0.0.0 --port 9000
```

## Структура проекта

```
.
├── alembic/              # миграции БД
├── repositories/         # работа с БД
├── routes/               # HTTP-эндпоинты
├── services/             # бизнес-логика
├── config.py             # настройки из env
├── database.py           # SQLAlchemy engine / session
├── main.py               # точка входа FastAPI
├── models.py             # модели User, Chat, Message
├── schemas.py            # Pydantic-схемы
├── Dockerfile
├── docker-compose.yaml
├── .env.example
└── requirements.txt
```

## Требования

- Docker и Docker Compose (рекомендуемый способ)
- либо Python 3.12+ и PostgreSQL 16

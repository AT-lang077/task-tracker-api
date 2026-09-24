# Task Tracker API

REST API для трекера задач: регистрация и авторизация пользователей, создание и управление задачами.

Стек: **Python, FastAPI, PostgreSQL, Docker, pytest**

## Возможности
- Регистрация `POST /auth/register` и логин `POST /auth/login` (JWT Bearer)
- Профиль `GET /users/me`
- CRUD задач `POST /tasks/`, `GET /tasks/`, `GET /tasks/{id}`, `PUT /tasks/{id}`, `DELETE /tasks/{id}`
- Фильтрация по статусу: `GET /tasks/?status=done` (`todo`, `in_progress`, `done`)
- Изоляция данных: каждый пользователь видит только свои задачи

## Быстрый старт (Docker — рекомендуется)

```bash
docker compose up --build
```

API будет доступно: http://localhost:8000
Документация Swagger: http://localhost:8000/docs

## Локальный запуск без Docker

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
# source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # Linux/Mac

# Для локального запуска без Postgres можно использовать SQLite:
# DATABASE_URL=sqlite:///./app.db

uvicorn app.main:app --reload
```

## Переменные окружения

| Переменная | Пример |
|---|---|
| `DATABASE_URL` | `postgresql://postgres:postgres@localhost:5432/tasktracker` |
| `SECRET_KEY` | `change-me-in-production-supersecret` |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` |

## Тесты

```bash
pytest -v
```

Покрыты ключевые сценарии: регистрация/логин, негативные кейсы (401/400/422), CRUD задач, фильтр по статусу, изоляция чужих задач.

## Пример запросов

```bash
# Регистрация
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"user@example.com\",\"password\":\"secret123\"}"

# Логин
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=secret123"

# Создать задачу (подставь TOKEN)
curl -X POST http://localhost:8000/tasks/ \
  -H "Authorization: Bearer TOKEN" -H "Content-Type: application/json" \
  -d "{\"title\":\"My task\",\"description\":\"Do it\"}"
```

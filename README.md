1. Клонируем и запускаем:
```bash
git clone <repo-url>
cd projectq
docker-compose up -d
```

2. Создаем `.env`:
```bash
DATABASE_NAME=projectq
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
```

## API Endpoints

### Комнаты (Rooms)
```bash
GET    /api/rooms/              # Список всех комнат
POST   /api/rooms/              # Создать комнату
GET    /api/rooms/{id}/         # Детали комнаты
PUT    /api/rooms/{id}/         # Обновить комнату
DELETE /api/rooms/{id}/         # Удалить комнату
GET    /api/rooms/{id}/availability  # Проверка доступности
```

Пример создания комнаты:
```json
{
  "name": "Переговорная 1",
  "capacity": 10,
  "equipment": ["проектор", "доска"]
}
```

### Бронирования (Bookings)
```bash
GET    /api/bookings/           # Все бронирования
POST   /api/bookings/           # Создать бронирование
GET    /api/bookings/{id}/      # Детали бронирования
DELETE /api/bookings/{id}/      # Отменить бронирование
```

Пример бронирования:
```json
{
  "room_id": 1,
  "start_time": "2024-03-20T14:00:00Z",
  "end_time": "2024-03-20T15:00:00Z",
  "purpose": "Встреча команды"
}
```

## Мониторинг
```bash
GET /health/  # Health check
```

## Технологии
- Python 3.12
- FastAPI
- PostgreSQL 15
- Docker & Docker Compose
- Gunicorn + Uvicorn

## Разработка

```bash
# Установка зависимостей
poetry install

# Тесты
poetry run pytest

# Запуск локально
poetry run python manage.py runserver
```

from src.routes import contacts as contacts_routes
from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
"""
Головний об'єкт додатку FastAPI, який використовується для додавання маршрутів і конфігурації середовища.
"""

app.include_router(contacts_routes.router, prefix="/api")
"""
Включення маршрутизатора контактів до основного додатку з префіксом '/api'.
"""

# Ініціалізація лімітера з використанням IP адреси клієнта як ключа
limiter = Limiter(key_func=get_remote_address)


# Підключення обробника для перевищення ліміту
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


origins = [
    "http://localhost:3000",  # Приклад, якщо ваш фронтенд працює на React і запущений на порту 3000
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""
Додає проміжне програмне забезпечення для управління CORS, дозволяючи запити з певних джерел.
"""

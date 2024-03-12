from src.routes import contacts as contacts_routes
from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Завантажує змінні середовища з .env файлу
load_dotenv()

# Тепер ви можете отримати змінні середовища за допомогою os.environ
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")


app = FastAPI()

app.include_router(contacts_routes.router, prefix="/api")


# Ініціалізація лімітера з використанням IP адреси клієнта як ключа
limiter = Limiter(key_func=get_remote_address)


# Підключення обробника для перевищення ліміту
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Список доменів, яким дозволено виконувати запити до вашого застосунку.
# Використовуйте зірочку "*", щоб дозволити всім доменам.
origins = [
    "http://localhost:3000",  # Приклад, якщо ваш фронтенд працює на React і запущений на порту 3000
    "https://yourfrontenddomain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Список джерел, які дозволено
    allow_credentials=True,  # Чи дозволено відправляти cookies
    allow_methods=["*"],  # Дозволені HTTP методи
    allow_headers=["*"],  # Дозволені HTTP заголовки
)


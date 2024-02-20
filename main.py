from fastapi import FastAPI
from src.routes import contacts as contacts_routes

app = FastAPI()

app.include_router(contacts_routes.router, prefix="/api")

# Додайте будь-які додаткові налаштування або маршрути, якщо потрібно

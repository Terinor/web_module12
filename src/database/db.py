from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Завантажуємо змінні середовища з .env файлу
load_dotenv()

# Отримуємо дані для підключення з змінних середовища
DATABASE_URL = f"postgresql://{os.getenv('postgresql_user')}:" \
               f"{os.getenv('postgresql_password')}@" \
               f"{os.getenv('postgresql_host')}:" \
               f"{os.getenv('postgresql_port')}/" \
               f"{os.getenv('postgresql_database')}"
"""
Глобальна змінна для зберігання URL підключення до бази даних, формується з змінних середовища.
"""
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

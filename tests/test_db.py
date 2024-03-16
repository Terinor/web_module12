import unittest
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv

class TestDatabaseConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Завантажуємо тестові змінні середовища
        load_dotenv(r"D:\projects\web\module11-12\tests\.env")

        DATABASE_URL = f"postgresql://{os.getenv('postgresql_user')}:" \
                    f"{os.getenv('postgresql_password')}@" \
                    f"{os.getenv('postgresql_host')}:" \
                    f"{os.getenv('postgresql_port')}/" \
                    f"{os.getenv('postgresql_database')}"
        cls.engine = create_engine(DATABASE_URL)
        cls.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls.engine)

    def test_create_session(self):
        # Перевірка, що сесія створюється без помилок
        session = self.SessionLocal()
        self.assertIsNotNone(session)

if __name__ == '__main__':
    unittest.main()

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
import os
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.database.models import User, Contact, Base

class TestModels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        load_dotenv(r"D:\projects\web\module11-12\tests\.env")

        DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:" \
                       f"{os.getenv('DB_PASSWORD')}@" \
                       f"{os.getenv('DB_HOST')}:" \
                       f"{os.getenv('DB_PORT')}/" \
                       f"{os.getenv('DB_TEST_NAME')}"
        cls.engine = create_engine(DATABASE_URL)
        cls.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls.engine)
        Base.metadata.create_all(bind=cls.engine)  # Створює всі таблиці

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(bind=cls.engine)  # Видаляє всі таблиці після тестування

    def setUp(self):
        self.db = self.SessionLocal()

    def tearDown(self):
        self.db.rollback()
        self.db.close()

    def test_create_user(self):
        new_user = User(email="test@example.com", hashed_password="hashedpassword")
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        self.assertEqual(new_user.email, "test@example.com")

    def test_unique_email_constraint(self):
        user1 = User(email="unique@example.com", hashed_password="password1")
        user2 = User(email="unique@example.com", hashed_password="password2")
        self.db.add(user1)
        self.db.commit()
        self.db.add(user2)
        with self.assertRaises(IntegrityError):
            self.db.commit()
        self.db.rollback()  # Важливо виконати rollback для очищення стану



if __name__ == '__main__':
    unittest.main()

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import unittest
from datetime import timedelta
from src.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token

class TestAuthUtils(unittest.TestCase):

    def setUp(self):
        self.plain_password = "secure_password"
        self.hashed_password = get_password_hash(self.plain_password)

    def test_password_hashing(self):
        # Переконуємося, що хеш паролю не дорівнює відкритому паролю
        self.assertNotEqual(self.hashed_password, self.plain_password)

    def test_verify_password(self):
        # Переконуємося, що функція верифікації паролю працює правильно
        self.assertTrue(verify_password(self.plain_password, self.hashed_password))

    def test_create_access_token(self):
        # Створюємо access token та перевіряємо, що він не пустий
        access_token = create_access_token(data={"sub": "user@example.com"})
        self.assertIsNotNone(access_token)
        self.assertIsInstance(access_token, str)

    def test_create_refresh_token(self):
        # Створюємо refresh token та перевіряємо, що він не пустий
        refresh_token = create_refresh_token(data={"sub": "user@example.com"})
        self.assertIsNotNone(refresh_token)
        self.assertIsInstance(refresh_token, str)

    def test_access_token_expiry(self):
        # Переконуємося, що токени мають час життя
        short_lived_token = create_access_token(data={"sub": "user@example.com"}, expires_delta=timedelta(minutes=1))
        default_lived_token = create_access_token(data={"sub": "user@example.com"})
        self.assertNotEqual(short_lived_token, default_lived_token)

if __name__ == "__main__":
    unittest.main()

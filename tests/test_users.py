import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session
from src.repository.users import create_user, authenticate_user, send_verification_email
from src.database.models import User
from src.schemas import UserCreate

class TestUserRepository(unittest.TestCase):

    def setUp(self):
        self.db = MagicMock(spec=Session)
        self.user_data = UserCreate(email="test@example.com", password="testpassword")
        self.user = User(email="test@example.com", hashed_password="hashed_testpassword")

    @patch("src.repository.users.get_password_hash")
    def test_create_user(self, mock_get_password_hash):
        mock_get_password_hash.return_value = "hashed_testpassword"
        self.db.add.return_value = None
        self.db.commit.return_value = None
        self.db.refresh.return_value = None
        self.db.query.return_value.filter.return_value.first.return_value = None

        # Додаємо фонове завдання без виклику асинхронної функції
        with patch('src.repository.users.BackgroundTasks.add_task') as mock_add_task:
            user = create_user(self.db, self.user_data, MagicMock())
            self.assertEqual(user.email, self.user_data.email)
            mock_get_password_hash.assert_called_once_with("testpassword")
            mock_add_task.assert_called_once()

    def test_authenticate_user(self):
        self.db.query.return_value.filter.return_value.first.return_value = self.user
        with patch("src.repository.users.verify_password") as mock_verify_password:
            mock_verify_password.return_value = True
            user = authenticate_user(self.db, "test@example.com", "testpassword")
            self.assertTrue(user)

    def test_authenticate_user_failure(self):
        self.db.query.return_value.filter.return_value.first.return_value = self.user
        with patch("src.repository.users.verify_password") as mock_verify_password:
            mock_verify_password.return_value = False
            user = authenticate_user(self.db, "test@example.com", "wrongpassword")
            self.assertFalse(user)


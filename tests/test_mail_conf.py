import unittest
from unittest.mock import patch
from src.mail.mail_conf import Environ, conf

class TestMailConfig(unittest.TestCase):
    @patch.dict('os.environ', {
        'MAIL_USERNAME': 'testuser@example.com',
        'MAIL_PASSWORD': 'testpassword',
        'MAIL_FROM': 'from@example.com',
        'MAIL_PORT': '587',
        'MAIL_SERVER': 'smtp.example.com',
        'MAIL_TLS': 'True',
        'MAIL_SSL': 'False',
        'SECRET_KEY': 'testsecretkey'
    })
    def test_environment_variables(self):
        # Перевіряємо, що змінні середовища коректно завантажуються
        self.assertEqual(Environ.MAIL_USERNAME, 'testuser@example.com')
        self.assertEqual(Environ.MAIL_PASSWORD, 'testpassword')
        self.assertEqual(Environ.MAIL_FROM, 'from@example.com')
        self.assertEqual(Environ.MAIL_PORT, 587)  # Переконуємося, що це ціле число
        self.assertEqual(Environ.MAIL_SERVER, 'smtp.example.com')
        self.assertTrue(Environ.MAIL_TLS)
        self.assertFalse(Environ.MAIL_SSL)
        self.assertEqual(Environ.SECRET_KEY, 'testsecretkey')

    def test_connection_config(self):
        # Перевіряємо, що ConnectionConfig правильно ініціалізований
        self.assertIsNotNone(conf)
        self.assertEqual(conf.MAIL_USERNAME, Environ.MAIL_USERNAME)
        self.assertEqual(conf.MAIL_PORT, Environ.MAIL_PORT)
        self.assertTrue(conf.USE_CREDENTIALS)
        self.assertTrue(conf.VALIDATE_CERTS)

if __name__ == '__main__':
    unittest.main()

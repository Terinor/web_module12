from fastapi.testclient import TestClient
from unittest import TestCase
import unittest
from main import app

class TestContactsRoutes(TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_create_contact(self):
        response = self.client.post("/contacts/", json={
            "first_name": "Test", "last_name": "User", "email": "test@example.com",
            "phone_number": "+1234567890", "birthday": "1990-01-01"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], "test@example.com")

    def test_read_contacts(self):
        response = self.client.get("/contacts/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_read_contact(self):
        response = self.client.get("/contacts/1")
        self.assertEqual(response.status_code, 200)

    def test_update_contact(self):
        response = self.client.put("/contacts/1", json={"first_name": "Updated", "last_name": "User"})
        self.assertEqual(response.status_code, 200)

    def test_delete_contact(self):
        response = self.client.delete("/contacts/1")
        self.assertEqual(response.status_code, 200)

    def test_search_contacts(self):
        response = self.client.get("/contacts/search/?query=Test")
        self.assertEqual(response.status_code, 200)

    def test_get_contacts_with_upcoming_birthdays(self):
        response = self.client.get("/contacts/upcoming-birthdays/")
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

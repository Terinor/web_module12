from fastapi.testclient import TestClient

from main import app
from ..src.database.db import Base, engine


client = TestClient(app)


Base.metadata.create_all(bind=engine)

def test_create_contact():
    response = client.post(
        "/contacts/",
        json={"first_name": "Test", "last_name": "User", "email": "test@example.com", "phone_number": "+1234567890", "birthday": "1990-01-01"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_read_contacts():
    response = client.get("/contacts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_contact():

    response = client.get("/contacts/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_update_contact():

    response = client.put(
        "/contacts/1",
        json={"first_name": "Updated", "last_name": "User"},
    )
    assert response.status_code == 200
    assert response.json()["first_name"] == "Updated"

def test_delete_contact():
    # Припустимо, що у вас уже є контакт з id=1 для видалення
    response = client.delete("/contacts/1")
    assert response.status_code == 200

def test_search_contacts():
    response = client.get("/contacts/search/?query=Test")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_contacts_with_upcoming_birthdays():
    response = client.get("/contacts/upcoming-birthdays/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

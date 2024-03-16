from fastapi.testclient import TestClient
from unittest.mock import patch
from src.main import app
from src.database.models import User
from sqlalchemy.orm import Session


client = TestClient(app)


@patch('src.routes.auth.create_user')
@patch('src.routes.auth.get_db')
def test_register_user(mock_get_db, mock_create_user):
    mock_session = Session()
    mock_get_db.return_value = mock_session
    mock_create_user.return_value = User(email="test@example.com")

    response = client.post("/register", json={
        "email": "test@example.com",
        "password": "password123"
    })

    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["token_type"] == "bearer"


@patch('src.routes.auth.authenticate_user')
@patch('src.routes.auth.get_db')
def test_login_for_access_token(mock_get_db, mock_authenticate_user):
    mock_session = Session()
    mock_get_db.return_value = mock_session
    mock_authenticate_user.return_value = User(email="test@example.com")

    response = client.post("/login", json={
        "email": "test@example.com",
        "password": "password123"
    })

    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["token_type"] == "bearer"


@patch('src.routes.auth.jwt.decode')
@patch('src.routes.auth.get_db')
def test_verify_email(mock_get_db, mock_jwt_decode):
    mock_session = Session()
    mock_get_db.return_value = mock_session
    mock_jwt_decode.return_value = {"sub": "test@example.com"}

    # Припустимо, що token='valid_token' - валідний токен для тесту
    response = client.get("/verify/valid_token")

    assert response.status_code == 200
    assert response.json() == {"message": "Email successfully verified."}

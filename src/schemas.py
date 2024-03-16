from pydantic import BaseModel, EmailStr, Field
from datetime import date


class ContactBase(BaseModel):
    """
    Базова модель контакту, яка описує основні поля, необхідні для контакту.
    """
    first_name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    email: EmailStr = Field(..., example="john.doe@example.com")
    phone_number: str = Field(..., example="+1234567890")
    birthday: date = Field(..., example="1990-01-01")


class ContactCreate(ContactBase):
    """
    Модель для створення нового контакту з необхідними полями.
    """
    pass


class ContactUpdate(ContactBase):
    """
    Модель для оновлення існуючого контакту. Включає всі поля з базової моделі.
    """
    pass


class Contact(ContactBase):
    """
    Розширена модель контакту, яка включає унікальний ідентифікатор контакту.
    """
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int = None

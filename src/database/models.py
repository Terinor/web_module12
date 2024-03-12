from sqlalchemy import Column, Integer, String, DateTime, Date,  Boolean
from .db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    refresh_token = Column(String, index=True, default=None)  # Додано поле для refresh токена
    token_expires = Column(DateTime, default=None)  # Час закінчення дії refresh токена
    is_active = Column(Boolean, default=False)  # Додано для верифікації електронної пошти

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    birthday = Column(Date)



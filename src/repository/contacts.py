from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime, timedelta
from ..database.models import Contact
from ..schemas import ContactCreate, ContactUpdate


def create_contact(db: Session, contact: ContactCreate):
    """
    Створює новий контакт в базі даних за допомогою наданих даних.

    :param db: Сесія бази даних.
    :param contact: Дані контакту для створення.
    :return: Інстанс створеного контакту.
    """
    new_contact = Contact(**contact.dict())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    """
    Повертає список контактів з бази даних, з можливістю пагінації.

    :param db: Сесія бази даних.
    :param skip: Кількість контактів, які потрібно пропустити для пагінації.
    :param limit: Максимальна кількість контактів, яка повертається.
    :return: Список контактів.
    """
    return db.query(Contact).offset(skip).limit(limit).all()


def get_contact_by_id(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()


def update_contact(db: Session, contact_id: int, contact: ContactUpdate):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        update_data = contact.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact


def search_contacts(db: Session, query: str, skip: int = 0, limit: int = 100):
    return db.query(Contact).filter(
        or_(
            Contact.first_name.ilike(f"%{query}%"),
            Contact.last_name.ilike(f"%{query}%"),
            Contact.email.ilike(f"%{query}%")
        )
    ).offset(skip).limit(limit).all()


def get_contacts_with_upcoming_birthdays(db: Session, days: int = 7, skip: int = 0, limit: int = 100):
    current_date = datetime.now().date()
    end_date = current_date + timedelta(days=days)
    return db.query(Contact).filter(
        and_(
            Contact.birthday >= current_date,
            Contact.birthday <= end_date
        )
    ).offset(skip).limit(limit).all()

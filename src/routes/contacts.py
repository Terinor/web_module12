from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from ..database.db import SessionLocal
from ..schemas import ContactCreate, Contact, ContactUpdate
from ..repository.contacts import (
    create_contact,
    get_contacts,
    get_contact_by_id,
    update_contact,
    delete_contact,
    search_contacts,
    get_contacts_with_upcoming_birthdays
)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=Contact)
def create_contact_route(contact: ContactCreate, db: Session = Depends(get_db)):
    return create_contact(db=db, contact=contact)


@router.get("/", response_model=List[Contact])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_contacts(db=db, skip=skip, limit=limit)


@router.get("/{contact_id}", response_model=Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = get_contact_by_id(db=db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.put("/{contact_id}", response_model=Contact)
def update_contact_route(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    updated_contact = update_contact(db=db, contact_id=contact_id, contact=contact)
    if updated_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact


@router.delete("/{contact_id}", response_model=Contact)
def delete_contact_route(contact_id: int, db: Session = Depends(get_db)):
    deleted_contact = delete_contact(db=db, contact_id=contact_id)
    if deleted_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return deleted_contact


@router.get("/search/", response_model=List[Contact])
def search_contacts_route(query: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return search_contacts(db=db, query=query, skip=skip, limit=limit)


@router.get("/upcoming-birthdays/", response_model=List[Contact])
def get_contacts_with_upcoming_birthdays_route(days: int = 7, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_contacts_with_upcoming_birthdays(db=db, days=days, skip=skip, limit=limit)

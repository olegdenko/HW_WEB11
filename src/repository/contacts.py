from fastapi import HTTPException
from datetime import datetime, timedelta
from typing import List
from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel, ContactUpdate, ContactStatusUpdate


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_upcoming_birthdays(db: Session) -> List[Contact]:
    today = datetime.now()
    end_date = today + timedelta(days=7)
    return (
        db.query(Contact)
        .filter(Contact.born_date >= today, Contact.born_date <= end_date)
        .all()
    )


async def get_contact(
    contact_id: int, name: str, last_name: str, e_mail: str, db: Session
) -> Contact:
    return (
        db.query(Contact)
        .filter(
            Contact.id == contact_id,
            Contact.name == name,
            Contact.last_name == last_name,
            Contact.e_mail == e_mail,
        )
        .first()
    )


async def search_contacts(
    name: str, last_name: str, e_mail: str, db: Session
) -> Contact:
    query = db.query(Contact)

    if name:
        query = query.filter(Contact.name.ilike(f"%{name}%"))
    if last_name:
        query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
    if e_mail:
        query = query.filter(Contact.e_mail.ilike(f"%{e_mail}%"))

    contacts = query.all()
    if name and last_name:
        contacts = [
            contact
            for contact in contacts
            if contact.name.lower() == name.lower()
            and contact.last_name.lower() == last_name.lower()
        ]

    if last_name and e_mail:
        contacts = [
            contact
            for contact in contacts
            if contact.last_name.lower() == last_name.lower()
            and contact.e_mail.lower() == e_mail.lower()
        ]

    return contacts


async def create_contact(body: ContactModel, db: Session) -> Contact:
    try:
        contact = Contact(
            name=body.name,
            last_name=body.last_name,
            e_mail=body.e_mail,
            phone_number=body.phone_number,
            born_date=datetime.strptime(body.born_date, "%d-%m-%Y"),
            description=body.description,
        )
        db.add(contact)
        db.commit()
        db.refresh(contact)
    except Exception:
        raise HTTPException(status_code=409)
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(
    contact_id: int, body: ContactUpdate, db: Session
) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.name = (body.name,)
        contact.last_name = (body.last_name,)
        contact.e_mail = (body.e_mail,)
        contact.phone_number = (body.phone_number,)
        contact.born_date = (body.born_date,)
        contact.description = (body.description,)
        db.commit()
    return contact


async def update_status_contact(
    contact_id: int, body: ContactStatusUpdate, db: Session
) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.done = body.done
        db.commit()
    return contact

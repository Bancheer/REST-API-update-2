from datetime import datetime, timedelta
from sqlalchemy import cast, Date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends
from contacts.contact import ContactSchema, ContactUpdateSchema
from models.model import Contact, User


async def create_contact(data: ContactSchema, user: User, db: AsyncSession):
    user = Contact(**data.model_dump(exclude_unset=True),user=user)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_contact(id: int, db:AsyncSession):
    stmt = select(Contact).filter_by(id=id)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user

async def get_contact_by_name(name: str, db: AsyncSession):
    stmt = select(Contact).filter_by(name=name)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user

async def get_contact_by_last_name(last_name: str, db: AsyncSession):
    stmt = select(Contact).filter_by(last_name=last_name)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user


async def get_contact_by_email(email: str, db: AsyncSession):
    stmt = select(Contact).filter_by(email=email)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user

async def get_contacts(db: AsyncSession):
    stmt = select(Contact)
    users = await db.execute(stmt)
    return users.scalars().all()


async def update_contact(data: ContactUpdateSchema, id: int, db: AsyncSession, user: User):
    stmt = select(Contact).filter(Contact.id == id, Contact.user == user)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(contact, key, value)
        await db.commit()
        await db.refresh(contact)
    return contact

async def delete_contact(id: int, db: AsyncSession):
    stmt = select(Contact).filter_by(id=id)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    if user:
        await db.delete(user)
        await db.commit()
    return user

async def birthday_seven(db: AsyncSession):
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    users = await db.execute(
        select(Contact).filter(
            cast(Contact.birthday, Date) >= today,
            cast(Contact.birthday, Date) <= next_week
        )
    )
    users = users.scalars().all()
    if not users:
        return {"message": "No users with birthdays in the next 7 days"}
    return users


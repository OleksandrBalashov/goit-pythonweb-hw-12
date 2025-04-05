from datetime import datetime, timedelta
from typing import Dict, Literal, Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.schemas.auth import User


from src.database.models import Contact
from src.schemas.schemas import ContactBase, ContactUpdate


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_contact_by_id(self, id: int, user: User) -> Contact | None:
        """
        Get a contact by its ID"
        Parameters:
        - id (int): ID of the contact.
        - user (User): Currently authenticated user.
        Returns:
        - Contact: The contact object if found, otherwise None.
        """
        stmt = select(Contact).filter_by(id=id, user=user)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()

    async def search_contacts(
        self,
        filters: Optional[Dict[str, str]],
        user: User,
    ) -> Sequence[Contact]:
        """
        Search for contacts based on the provided filters.
        Parameters:
        - filters (Dict[str, str]): Dictionary of filters to apply.
        - user (User): Currently authenticated user.
        Returns:
        - List[Contact]: List of contacts matching the filters.
        """
        stmt = select(Contact)

        for field, value in filters.items():
            if value:
                stmt = stmt.where(getattr(Contact, field).ilike(f"%{value}%"))

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_contacts(
        self, limit: int, offset: int, user: User
    ) -> Sequence[Contact]:
        """
        Get a list of contacts with pagination.
        Parameters:
        - limit (int): Number of contacts to return.
        - offset (int): Number of contacts to skip.
        - user (User): Currently authenticated user.
        Returns:
        - List[Contact]: List of contacts.
        """
        stmt = select(Contact).filter_by(user=user).offset(offset).limit(limit)
        contacts = await self.db.execute(stmt)
        return list(contacts.scalars().all())

    async def create_contact(self, contact: ContactBase, user: User) -> Contact:
        """
        Create a new contact.
        Parameters:
        - contact (ContactBase): Contact data to create.
        - user (User): Currently authenticated user.
        Returns:
        - Contact: The created contact object.
        """
        new_contact = Contact(**contact.model_dump(exclude_unset=True), user=user)
        self.db.add(new_contact)
        await self.db.commit()
        await self.db.refresh(new_contact)
        return new_contact

    async def update_contact(
        self, id: int, body: ContactUpdate, user: User
    ) -> Contact | None:
        """
        Update an existing contact.
        Parameters:
        - id (int): ID of the contact to update.
        - body (ContactUpdate): Updated contact data.
        - user (User): Currently authenticated user.
        Returns:
        - Contact: The updated contact object if found, otherwise None.
        """
        contact = await self.get_contact_by_id(id, user)
        if contact:
            contact.name = body.name
            contact.last_name = body.last_name
            contact.email = body.email
            contact.phone = body.phone
            contact.birthday = body.birthday
            contact.additional_data = body.additional_data

            await self.db.commit()
            await self.db.refresh(contact)
        return contact

    async def delete_contact(self, id: int, user: User) -> Contact:
        """
        Delete a contact by its ID.
        Parameters:
        - id (int): ID of the contact to delete.
        - user (User): Currently authenticated user.
        Returns:
        - Contact: The deleted contact object if found, otherwise None.
        """
        contact = await self.get_contact_by_id(id, user)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def get_upcoming_birthdays(self, user: User, limit: int = 100):
        """
        Get contacts with upcoming birthdays within the next 7 days.
        Parameters:
        - user (User): Currently authenticated user.
        - limit (int): Maximum number of contacts to return.
        Returns:
        - List[Contact]: List of contacts with upcoming birthdays.
        Raises:
        - ValueError: If the limit is less than 1.
        """
        today = datetime.today().date()
        seven_days_later = today + timedelta(days=7)

        stmt = (
            select(Contact)
            .filter_by(user=user)
            .filter(Contact.birthday >= today)
            .filter(Contact.birthday <= seven_days_later)
            .order_by(Contact.birthday)
            .limit(limit)
        )

        result = await self.db.execute(stmt)
        return result.scalars().all()

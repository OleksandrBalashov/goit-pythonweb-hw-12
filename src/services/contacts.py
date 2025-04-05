from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.contacts import ContactRepository
from src.schemas.auth import User


class ContactService:
    """
    Service class for managing contacts.
    It provides methods to interact with the ContactRepository
    and perform operations related to contacts.
    """

    def __init__(self, db: AsyncSession):
        self.contact_repository = ContactRepository(db)

    async def get_contacts(self, limit: int, offset: int, user: User):
        """
        Get a list of contacts with pagination.
        Parameters:
        - limit (int): Number of contacts to return."
        - offset (int): Number of contacts to skip.
        - user (User): Currently authenticated user.
        Returns:
        - List[Contact]: List of contacts.
        """
        return await self.contact_repository.get_contacts(limit, offset, user)

    async def get_contact_by_id(self, id: int, user: User):
        """
        Get a contact by its ID.
        Parameters:
        - id (int): ID of the contact.
        - user (User): Currently authenticated user.
        Returns:
        - Contact: The contact object if found, otherwise None.
        """
        return await self.contact_repository.get_contact_by_id(id, user)

    async def search_contacts(self, field: str, user: User):
        """
        Search for contacts based on the provided filters.
        Parameters:
        - field (str): Field to search for.
        - user (User): Currently authenticated user.
        Returns:
        - List[Contact]: List of contacts matching the filters.
        """
        return await self.contact_repository.search_contacts(field, user)

    async def create_contact(self, contact, user: User):
        """
        Create a new contact.
        Parameters:
        - contact (ContactBase): Contact creation data.
        - user (User): Currently authenticated user.
        Returns:
        - Contact: The created contact object.
        """
        return await self.contact_repository.create_contact(contact, user)

    async def update_contact(self, id: int, body, user: User):
        """
        Update an existing contact.
        Parameters:
        - id (int): ID of the contact to update.
        - body (ContactBase): Updated contact data.
        - user (User): Currently authenticated user.
        Returns:
        - Contact: The updated contact object.
        """
        return await self.contact_repository.update_contact(id, body, user)

    async def delete_contact(self, id: int, user: User):
        """
        Delete a contact by its ID.
        Parameters:"
        - id (int): ID of the contact to delete."
        - user (User): Currently authenticated user.
        Returns:
        - bool: True if the contact was deleted, False otherwise.
        """
        return await self.contact_repository.delete_contact(id, user)

    async def get_upcoming_birthdays(
        self,
        user: User,
        limit: int,
    ):
        """
        Get contacts with upcoming birthdays within the next 7 days.
        Parameters:
        - user (User): Currently authenticated user.
        - limit (int): Number of contacts to return.
        Returns:
        - List[Contact]: List of contacts with upcoming birthdays.
        """
        return await self.contact_repository.get_upcoming_birthdays(user, limit)

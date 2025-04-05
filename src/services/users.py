from sqlalchemy.ext.asyncio import AsyncSession

from libgravatar import Gravatar

from src.repository.users import UserRepository
from src.schemas.auth import UserCreate


class UserService:
    """
    Service class for managing users.
    It provides methods to interact with the UserRepository
    and perform operations related to users.
    """

    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)

    async def create_user(self, body: UserCreate):
        """
        Create a new user.
        Parameters:
        - body (UserCreate): User creation data.
        Returns:
        - User: The created user object.
        """
        # Generate Gravatar URL'
        avatar = None
        try:
            g = Gravatar(body.email)
            avatar = g.get_image()
        except Exception as e:
            print(e)

        return await self.repository.create_user(body, avatar)

    async def get_user_by_id(self, user_id: int):
        """
        Get a user by their ID.
        Parameters:
        - user_id (int): ID of the user.
        Returns:
        - User: The user object if found, otherwise None.
        """
        return await self.repository.get_user_by_id(user_id)

    async def get_user_by_username(self, username: str):
        """
        Get a user by their username.
        Parameters:
        - username (str): Username of the user.
        Returns:
        - User: The user object if found, otherwise None.
        """
        return await self.repository.get_user_by_username(username)

    async def get_user_by_email(self, email: str):
        """
        Get a user by their email.
        Parameters:
        - email (str): Email of the user.
        Returns:
        - User: The user object if found, otherwise None.
        """
        return await self.repository.get_user_by_email(email)

    async def confirmed_email(self, email: str):
        """
        Confirm a user's email address.
        Parameters:
        - email (str): Email of the user.
        Returns:
        - None
        """
        return await self.repository.confirmed_email(email)

    async def update_avatar_url(self, email: str, url: str):
        """
        Update the user's avatar URL.
        Parameters:
        - email (str): Email of the user.
        - url (str): New avatar URL.
        Returns:
        - User: The updated user object.
        """
        return await self.repository.update_avatar_url(email, url)

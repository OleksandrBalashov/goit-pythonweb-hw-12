from datetime import datetime, timedelta, UTC
from typing import Optional
from aiocache import cached

from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from src.database.db import get_db
from src.config.config import config
from src.services.users import UserService
from src.database.models import User, UserRole


class Hash:
    """ "
    Hashing class for password hashing and verification.
    """

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        """
        Verify the provided password against the hashed password.
        Parameters:
        - plain_password (str): The password to verify.
        - hashed_password (str): The hashed password to compare against.
        Returns:
        - bool: True if the password matches, False otherwise.
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        """
        Hash the provided password.
        Parameters:
        - password (str): The password to hash.
        Returns:
        - str: The hashed password.
        """
        return self.pwd_context.hash(password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def create_access_token(data: dict, expires_delta: Optional[int] = None):
    """
    Create a JWT access token.
    Parameters:
    - data (dict): Data to encode in the token.
    - expires_delta (int): Expiration time in seconds.
    Returns:
    - str: The encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + timedelta(seconds=expires_delta)
    else:
        expire = datetime.now(UTC) + timedelta(seconds=config.JWT_EXPIRATION_SECONDS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM
    )
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get the current user from the JWT token.
    Parameters:
    - token (str): The JWT token.
    - db (AsyncSession): The database session.
    Returns:
    - User: The user object.
    Raises:
    - HTTPException (401): If the token is invalid or user not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM]
        )
        username = payload["sub"]
        if username is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception
    user_service = UserService(db)
    user = await user_service.get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user


def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Get the current user with admin role.
    Parameters:
    - current_user (User): The current user object.
    Returns:
    - User: The user object with admin role.
    Raises:
    - HTTPException (403): If the user is not an admin.
    403: Permission denieds
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Permission denied")
    return current_user


def cache_key_builder(func, args, kwargs) -> str:
    """
    Build a cache key for the user based on the username.
    Parameters:
    - func: The function being cached.
    - args: The positional arguments passed to the function.
    """
    return f"username: {args[0]}"


@cached(ttl=300, key_builder=cache_key_builder)
async def get_user_from_db(username: str, db: AsyncSession) -> User:
    """
    Отримує користувача з бази даних, використовуючи кешування.
    """
    print("NOT CACHED USER")
    user_service = UserService(db)
    user = await user_service.get_user_by_username(username)
    return user


def create_email_token(data: dict):
    """
    Create a JWT token for email confirmation.
    Parameters:
    - data (dict): Data to encode in the token.
    Returns:"
    - str: The encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(days=7)
    to_encode.update({"iat": datetime.now(UTC), "exp": expire})
    token = jwt.encode(to_encode, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)
    return token


async def get_email_from_token(token: str):
    """ "
    Decode the JWT token to get the email.
    Parameters:
    - token (str): The JWT token to decode.
    Returns:
    - str: The email extracted from the token.
    Raises:
    - HTTPException (422): If the token is invalid.
    """
    try:
        payload = jwt.decode(
            token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM]
        )
        email = payload["sub"]
        return email
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Неправильний токен для перевірки електронної пошти",
        )


async def get_password_from_token(token: str) -> str:
    """
    Decode the JWT token to get the password.
    Parameters:
    - token (str): The JWT token to decode.
    Returns:
    - str: The password extracted from the token.
    Raises:
    - HTTPException (422): If the token is invalid
    """
    try:
        payload = jwt.decode(
            token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM]
        )
        password = payload["password"]
        return password
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Wrong token",
        )

from typing import Optional
from enum import Enum

from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, relationship
from sqlalchemy import (
    Date,
    Enum as SQLAlchemyEnum,
    ForeignKey,
    Integer,
    String,
    Boolean,
    Column,
    DateTime,
    func,
)


class Base(DeclarativeBase):
    pass


class Contact(Base):
    """
    Represents a contact in the database.
    Attributes:
        id (int): Unique identifier for the contact.
        name (str): Name of the contact.
        last_name (str): Last name of the contact.
        email (str): Email address of the contact.
        phone (str): Phone number of the contact.
        birthday (Date): Birthday of the contact.
        additional_data (Optional[str]): Additional data related to the contact.
        user_id (int): Foreign key referencing the user who owns this contact.
        user (User): Relationship to the User model.
    """

    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(128), nullable=False)
    birthday: Mapped[Date] = mapped_column(Date, nullable=False)
    additional_data: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    user_id = Column(
        "user_id", ForeignKey("users.id", ondelete="CASCADE"), default=None
    )
    user = relationship("User", backref="contacts")


class UserRole(str, Enum):
    """
    Enum representing user roles.
    Attributes:
        USER (str): Regular user role.
        ADMIN (str): Administrator role.
    """

    ADMIN = "admin"
    USER = "user"


class User(Base):
    """
    Represents a user in the database.
    Attributes:
        id (int): Unique identifier for the user.
        username (str): Username of the user.
        email (str): Email address of the user.
        hashed_password (str): Hashed password of the user.
        created_at (DateTime): Timestamp when the user was created.
        avatar (Optional[str]): URL of the user's avatar.
        confirmed (bool): Indicates whether the user's email is confirmed.
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
    role = Column(SQLAlchemyEnum(UserRole), default=UserRole.USER, nullable=False)

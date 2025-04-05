from pydantic import BaseModel
from datetime import date
from typing import Optional

from pydantic import Field, EmailStr


class ContactBase(BaseModel):
    """
    ContactBase schema for Pydantic validation.
    Attributes:
        name (str): Name of the contact.
        last_name (str): Last name of the contact.
        email (str): Email address of the contact.
        phone (str): Phone number of the contact.
        birthday (Optional[date]): Birthday of the contact.
        additional_data (Optional[str]): Additional data about the contact.
    """

    name: str
    last_name: str
    email: str
    phone: str
    birthday: Optional[date] = None
    additional_data: Optional[str] = None


class ContactResponse(ContactBase):
    """
    ContactResponse schema for Pydantic validation.
    Attributes:
        id (int): Unique identifier for the contact.
    """

    id: int


class ContactUpdate(ContactBase):
    """
    ContactUpdate schema for Pydantic validation."
    Attributes:
        name (Optional[str]): Name of the contact.
        last_name (Optional[str]): Last name of the contact.
        email (Optional[str]): Email address of the contact.
        phone (Optional[str]): Phone number of the contact.
    """

    name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class ContactSearchParams(BaseModel):
    """
    ContactSearchParams schema for Pydantic validation.
    Attributes:
        name (Optional[str]): Name of the contact.
        email (Optional[str]): Email address of the contact.
        last_name (Optional[str]): Last name of the contact.
    """

    name: Optional[str] = None
    email: Optional[str] = None
    last_name: Optional[str] = None


class Contact(ContactBase):
    """
    Contact schema for Pydantic validation.
    Attributes:
        id (int): Unique identifier for the contact.
    """

    id: int

    class Config:
        from_attributes = True


class ResetPassword(BaseModel):
    """
    ResetPassword schema for Pydantic validation.
    Attributes:
        email (EmailStr): User's email address.
        password (str): New password for the user.
    """

    email: EmailStr
    password: str = Field(min_length=4, max_length=128, description="Новий пароль")

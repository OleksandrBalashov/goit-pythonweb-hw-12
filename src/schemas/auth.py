from pydantic import BaseModel, Field, ConfigDict, EmailStr


class User(BaseModel):
    """
    User schema for Pydantic validation."
    Attributes:
        id (int): Unique identifier for the user.
        username (str): Username of the user.
        email (EmailStr): Email address of the user.
        avatar (str): URL of the user's avatar.
    """

    id: int
    username: str = Field(min_length=2, max_length=50, description="Username")
    email: EmailStr
    avatar: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(User):
    """
    User creation schema for Pydantic validation.
    Inherits from User and adds a password field.
    Attributes:
        password (str): Password for the user.
    """

    password: str = Field(min_length=6, max_length=12, description="Password")

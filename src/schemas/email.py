from pydantic import BaseModel, EmailStr


class RequestEmail(BaseModel):
    """
    RequestEmail schema for Pydantic validation.
    Attributes:
        email (EmailStr): Email address of the user.
    """

    email: EmailStr

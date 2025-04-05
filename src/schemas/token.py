from pydantic import BaseModel


class Token(BaseModel):
    """
    Token schema for Pydantic validation.
    """

    token: str
    token_type: str

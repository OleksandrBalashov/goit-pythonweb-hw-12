from fastapi import APIRouter, Depends, Request, UploadFile, File
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas.auth import User
from src.services.auth import get_current_admin_user, get_current_user
from src.config.config import config
from src.services.uplaod import UploadFileService
from src.services.users import UserService

router = APIRouter(prefix="/users", tags=["users"])
limiter = Limiter(key_func=get_remote_address)


@router.get(
    "/me", response_model=User, description="No more than 10 requests per minute"
)
@limiter.limit("10/minute")
async def me(request: Request, user: User = Depends(get_current_user)):
    """
    This endpoint retrieves the details of the currently authenticated user.
    It is rate-limited to prevent abuse.

    Limitations:
    - Rate-limited to 10 requests per minute.

    Parameters:
    - request (Request): The HTTP request object.
    - user (User): The currently authenticated user.

    Retruns:
    - User: The details of the authenticated user.
    """
    return user


@router.patch("/avatar", response_model=User)
async def update_avatar_user(
    file: UploadFile = File(),
    user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """
    This endpoint allows the Admin to update their avatar.

    Parameters:
    - file (UploadFile): The new avatar file to be uploaded.
    - user (User): The currently authenticated Admin.
    - db (AsyncSession): The database session.
    Returns:
    - User: The updated user details with the new avatar URL.
    Raises:
    - HTTPException: If no file is uploaded or if the upload fails.
    """
    if not file:
        return {"message": "No file uploaded"}
    avatar_url = UploadFileService(
        config.CLD_NAME, config.CLD_API_KEY, config.CLD_API_SECRET
    ).upload_file(file, user.username)

    user_service = UserService(db)
    user = await user_service.update_avatar_url(user.email, avatar_url)

    return user

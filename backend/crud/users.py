import os
from pathlib import Path
import shutil
from typing import Optional, List
from fastapi import Depends, HTTPException, UploadFile, status, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from jose import JWTError, jwt
import ulid
from ..db import models, get_db
from ..schemas import users as user_schemas
from ..core import auth
from ..core.auth import oauth2_scheme, SECRET_KEY, ALGORITHM

# Resolve the path to the backend directory
BASE_DIR = Path(__file__).resolve().parent.parent
ICON_DIR = BASE_DIR / "static/icons"
ICON_DIR.mkdir(parents=True, exist_ok=True)

def create_user(db: Session,
                user: user_schemas.UserCreate,
                google_login: bool = False) -> models.User:
    """
    Creates a new user in the database.

    Args:
        db (Session): The database session.
        user (UserCreate): The user creation schema.
        google_login (bool): Whether the user is a Google login user.

    Returns:
        User: The created user instance.
    """
    hashed_password = auth.hash_password(user.password) if user.password else None
    uid = str(ulid.new())
    db_user = models.User(
        username=user.username,
        uid=uid,
        email=user.email,
        password=hashed_password,
        icon=user.icon,
        google_login=google_login
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(
        db: Session,
        user_id: int,
        user_update: user_schemas.UserUpdate) -> Optional[models.User]:
    """
    Updates an existing user's details in the database.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to update.
        user_update (UserUpdate): The updated user data.

    Returns:
        User or None: The updated user instance or None if not found.
    """
    # Retrieve the user from the database
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        # Use model_dump(exclude_unset=True) to include only provided fields
        update_data = user_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)

        # Commit the changes to the database
        db.commit()
        db.refresh(db_user)
    return db_user

def update_password(
        db: Session,
        user_id: int,
        new_password: str) -> Optional[models.User]:
    """
    Updates an existing user's password in the database.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to update.
        new_password (str): The new password to set.

    Returns:
        User or None: The updated user instance or None if not found.
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        try:
            hashed_password = auth.hash_password(new_password)
            db_user.password = hashed_password
            db.commit()
            db.refresh(db_user)
        except JWTError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "code": "AUTH_001",
                    "message": "Invalid token."
                },
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc
        except SQLAlchemyError as exc:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "code": "SRV_002",
                    "message": "An unexpected database error occurred."
                }
            ) from exc
    return db_user

def update_user_icon(
    db: Session,
    user_id: int,
    file: UploadFile,
    background_tasks: BackgroundTasks,
) -> dict:
    """
    Updates a user's profile icon.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user whose icon is being updated.
        file (UploadFile): The uploaded image file.
        background_tasks (BackgroundTasks): To handle image cleanup.

    Returns:
        dict: Success message and new icon URL.
    """
    # Fetch the user
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")

    # Generate a unique filename
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{user.uid}_{ulid.new()}.{file_extension}"
    file_path = ICON_DIR / unique_filename

    # Save the new icon
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Schedule old icon cleanup if it exists and is not the default icon
    if user.icon and user.icon != "default.png":
        old_icon_path = ICON_DIR / user.icon
        if old_icon_path.exists():
            background_tasks.add_task(os.remove, old_icon_path)

    # Update user's icon in the database
    user.icon = unique_filename
    db.commit()
    db.refresh(user)

    return {"message": "Profile icon updated successfully", "icon_url": f"/icons/{unique_filename}"}

def delete_user(db: Session, user_id: int) -> Optional[models.User]:
    """
    Deletes an existing user from the database.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to delete.

    Returns:
        User or None: The deleted user instance or None if not found.
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        if db_user.icon and db_user.icon != "default.png":
            background_tasks = BackgroundTasks()
            icon_path = ICON_DIR / db_user.icon
            if icon_path.exists():
                background_tasks.add_task(os.remove, icon_path)

        db.delete(db_user)
        db.commit()
    return db_user

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Retrieves the current user based on the provided JWT access token.

    Args:
        token (str): JWT access token from the Authorization header.
        db (Session): Database session dependency.

    Raises:
        HTTPException: If the token is invalid or user is not found.

    Returns:
        models.User: The current authenticated user.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "code": "AUTH_003",
                    "message": "Invalid token: missing email."
                },
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = get_user_by_email(db, email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": "USER_001",
                    "message": "User not found."
                },
            )
        return user
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "AUTH_001",
                "message": "Invalid token."
            },
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """
    Fetches a user by their username.

    Args:
        db (Session): The database session.
        username (str): The username of the user.

    Returns:
        User or None: The fetched user or None if not found.
    """
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_uid(db: Session, uid: str) -> Optional[models.User]:
    """
    Fetches a user by their uid.

    Args:
        db (Session): The database session.
        uid (str): The uid of the user.

    Returns:
        User or None: The fetched user or None if not found.
    """
    return db.query(models.User).filter(models.User.uid == uid).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    """
    Fetches a user by their id.

    Args:
        db (Session): The database session.
        id (int): The id of the user.

    Returns:
        User or None: The fetched user or None if not found.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """
    Fetches a user by their email.

    Args:
        db (Session): The database session.
        email (str): The email of the user.

    Returns:
        User or None: The fetched user or None if not found.
    """
    return db.query(models.User).filter(models.User.email == email).first()

def get_all_users(db: Session) -> List[models.User]:
    """
    Retrieves all users from the database.

    Args:
        db (Session): The database session.

    Returns:
        List[User]: A list of all user instances.
    """
    return db.query(models.User).all()

def get_users_by_ids(db: Session, user_ids: List[int]) -> List[models.User]:
    """
    Fetches multiple users by their IDs.

    Args:
        db (Session): The database session.
        user_ids (List[int]): List of user IDs.

    Returns:
        List[User]: A list of users matching the given IDs.
    """
    return db.query(models.User).filter(models.User.id.in_(user_ids)).all()

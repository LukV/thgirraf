from typing import Optional, List
from sqlalchemy.orm import Session
from ..db import models
from ..schemas import users as user_schemas
from ..core import auth

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
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        google_login=google_login
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session,
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
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        for key, value in user_update.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

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
        db.delete(db_user)
        db.commit()
    return db_user

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

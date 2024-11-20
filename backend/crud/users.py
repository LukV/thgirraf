from typing import Optional, List
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import ulid
from ..db import models, get_db
from ..schemas import users as user_schemas
from ..core import auth
from ..core.auth import oauth2_scheme, SECRET_KEY, ALGORITHM

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
                detail="Invalid token: missing email",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = get_user_by_email(db, email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
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

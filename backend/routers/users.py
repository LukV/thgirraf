from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import users as user_schemas
from ..crud import users as crud_users
from ..core import auth
from ..db.database import get_db


router = APIRouter()

@router.get("/me", response_model=user_schemas.UserResponse)
def read_current_user(current_user: user_schemas.UserResponse = Depends(crud_users.get_current_user)):
    """
    Retrieves the currently authenticated user.

    Returns:
        UserResponse: The current user's data.
    """
    return current_user

@router.post("/", response_model=user_schemas.UserResponse)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user in the database.

    Raises:
        HTTPException: If the username or email is already registered.

    Returns:
        UserResponse: The created user data.
    """
    if crud_users.get_user_by_username(db, user.username) \
            or crud_users.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Username or email already registered")
    return crud_users.create_user(db, user)

@router.get("/", response_model=List[user_schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """
    Retrieve a list of all users in the database.

    Returns:
        List[UserResponse]: A list of user data.
    """
    return crud_users.get_all_users(db)

@router.put("/{user_id}", response_model=user_schemas.UserResponse)
def update_user(user_id: int, user_update: user_schemas.UserUpdate, db: Session = Depends(get_db)):
    """
    Update an existing user's details.

    Returns:
        UserResponse: The updated user data.
    """
    return crud_users.update_user(db, user_id, user_update)

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete an existing user from the database.

    Returns:
        dict: Success message upon deletion.
    """
    crud_users.delete_user(db, user_id)
    return {"message": "User deleted successfully"}

@router.post("/reset-password")
def reset_password(username: str, new_password: str, db: Session = Depends(get_db)):
    """
    Reset a user's password.

    Raises:
        HTTPException: If the user is not found in the database.

    Returns:
        dict: Success message upon successful password reset.
    """
    user = crud_users.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.password = auth.hash_password(new_password)
    db.commit()
    return {"message": "Password reset successfully"}

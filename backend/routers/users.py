from typing import List
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt
from ..schemas import users as user_schemas
from ..crud import users as crud_users
from ..core import auth, email_service
from ..db.database import get_db


router = APIRouter()

@router.get("/me", response_model=user_schemas.UserResponse)
def read_current_user(current_user: \
                      user_schemas.UserResponse = Depends(crud_users.get_current_user)):
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

@router.post("/request-password-reset")
def request_password_reset(
    payload: user_schemas.PasswordResetRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Request a password reset by sending a reset link to the user's email.

    Returns:
        dict: Success message upon email sent.
    """
    user = crud_users.get_user_by_email(db, email=payload.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate a token (JWT or secure random string) with an expiry
    token = auth.create_password_reset_token(user.uid)
    # Add the email sending task to the background
    background_tasks.add_task(email_service.send_reset_email, payload.email, token)

    return {"message": "Password reset email sent"}


@router.post("/reset-password")
def reset_password(
    payload: user_schemas.PasswordReset,
    db: Session = Depends(get_db)
):
    """
    Reset a user's password using a token for validation.

    Returns:
        dict: Success message upon successful password reset.
    """
    # Validate the token
    try:
        # Decode the token using the auth module
        payload_data = jwt.decode(payload.token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        user_uid = payload_data.get("sub")
    except jwt.JWTError as exc:
        raise HTTPException(status_code=400, detail="Invalid or expired token") from exc

    # Verify that the email and user_uid match
    user = crud_users.get_user_by_email(db, email=payload.email)
    if not user or str(user.uid) != user_uid:
        raise HTTPException(status_code=404, detail="User not found or email does not match token")

    # Hash the new password and save it using auth's hash_password function
    user.password = auth.hash_password(payload.new_password)
    db.commit()
    return {"message": "Password reset successfully"}


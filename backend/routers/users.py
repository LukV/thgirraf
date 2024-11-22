from typing import List
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Body,
    Depends,
    HTTPException,
    UploadFile,
    File
)
from sqlalchemy.orm import Session
from jose import jwt
from ..schemas import users as user_schemas
from ..crud import users as crud_users
from ..crud.users import get_current_user
from ..core import auth, utils
from ..db import models
from ..db.database import get_db

router = APIRouter()

@router.post("/", response_model=user_schemas.UserResponse)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user in the database."""
    if crud_users.get_user_by_username(db, user.username) \
            or crud_users.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Username or email already registered.")
    return crud_users.create_user(db, user)

@router.get("/", response_model=List[user_schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """Retrieve a list of all users in the database."""
    return crud_users.get_all_users(db)

@router.post("/batch", response_model=List[user_schemas.UserResponse])
def batch_get_users(user_ids: List[int] = Body(...), db: Session = Depends(get_db)):
    """Retrieve multiple users by their IDs."""
    users = crud_users.get_users_by_ids(db, user_ids)
    return users

@router.get("/me", response_model=user_schemas.UserResponse)
def read_current_user(current_user: \
                      user_schemas.UserResponse = Depends(crud_users.get_current_user)):
    """Retrieves the currently authenticated user."""
    return current_user

@router.get("/{user_id}", response_model=user_schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Update an existing user's details."""
    return crud_users.get_user_by_id(db, user_id)

@router.put("/{user_id}", response_model=user_schemas.UserResponse)
def update_user(user_id: int, user_update: user_schemas.UserUpdate, db: Session = Depends(get_db)):
    """Update an existing user's details."""
    return crud_users.update_user(db, user_id, user_update)

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete an existing user from the database. This is a hard delete."""
    crud_users.delete_user(db, user_id)
    return "User deleted successfully"

@router.put("/{user_id}/icon")
def upload_icon(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    """Upload or replace a user's profile icon."""
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    return crud_users.update_user_icon(
        db=db,
        user_id=user_id,
        file=file,
        background_tasks=background_tasks,
    )

@router.post("/request-password-reset")
def request_password_reset(
    payload: user_schemas.PasswordResetRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Request a password reset by sending a reset link to the user's email. 
    Relies on a utility function tied to a specific smtp service, eg AWS SES.
    See GH for details.
    """
    user = crud_users.get_user_by_email(db, email=payload.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    # Generate a token with an expiry
    token = auth.create_password_reset_token(user.uid)

    # Add the email sending task to the background
    background_tasks.add_task(utils.send_reset_email, payload.email, token)

    return "Password reset email sent."

@router.post("/reset-password")
def reset_password(
    payload: user_schemas.PasswordReset,
    db: Session = Depends(get_db)
):
    """Reset a user's password using a token for validation."""
    try:
        # Decode the token using the auth module
        payload_data = jwt.decode(payload.token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        user_uid = payload_data.get("sub")
    except jwt.JWTError as exc:
        raise HTTPException(status_code=400, detail="Invalid or expired token.") from exc

    # Verify that the email and user_uid match
    user = crud_users.get_user_by_email(db, email=payload.email)
    if not user or str(user.uid) != user_uid:
        raise HTTPException(status_code=404,
                            detail="User not found, or email does not match token.")

    user.password = auth.hash_password(payload.new_password)
    db.commit()
    return {
        "code": "AUTH_004",
        "message": "Password reset successfully",
    }

@router.post("/change-password")
def change_password(
    request: user_schemas.PasswordChange,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Endpoint to update the password for the authenticated user."""
    updated_user = crud_users.update_password(
        db=db,
        user_id=current_user.id,
        new_password=request.new_password
    )
    if not updated_user:
        raise HTTPException(status_code=404,
                            detail="User not found or password could not be updated.")
    return "Password updated successfully."

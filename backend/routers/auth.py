from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from ..core import auth
from ..core.utils import download_user_icon
from ..crud import users as crud_users
from ..db.database import get_db
from ..schemas.users import UserCreate
from ..schemas.auth import TokenPair, LoginRequest

router = APIRouter()

@router.post("/login", response_model=TokenPair)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """Endpoint for user login with either Firebase token or credentials.

    Raises:
        HTTPException: 400 error if login credentials are missing.
        HTTPException: 400 error if credentials are invalid.

    Returns:
        dict: Access and refresh tokens with token type.
    """
    if login_data.token:  # Google login
        google_user_data = auth.verify_firebase_token(login_data.token)
        user = crud_users.get_user_by_email(db, google_user_data["email"])
        google_picture_url = google_user_data.get("picture")

        if not user:
            icon_path = download_user_icon(google_picture_url, google_user_data["uid"]) if google_picture_url else None
            new_user_data = UserCreate(
                username=google_user_data["name"],
                email=google_user_data["email"],
                icon=icon_path
            )
            user = crud_users.create_user(db, user=new_user_data, google_login=True)

        # Generate access and refresh tokens
        access_token = auth.create_access_token(data={"sub": user.email})
        refresh_token = auth.create_refresh_token(data={"sub": user.email}) # pylint: disable=W0621
        return {
            "access_token": access_token, 
            "refresh_token": refresh_token, 
            "token_type": "bearer"
        }

    elif login_data.username and login_data.password:  # Standard login
        user = crud_users.get_user_by_username(db, login_data.username) or \
               crud_users.get_user_by_email(db, login_data.username)

        if not user or not auth.verify_password(login_data.password, user.password):
            raise HTTPException(status_code=400, detail="Invalid credentials")

        # Generate access and refresh tokens
        access_token = auth.create_access_token(data={"sub": user.email})
        refresh_token = auth.create_refresh_token(data={"sub": user.email})
        return {
            "access_token": access_token, 
            "refresh_token": refresh_token, 
            "token_type": "bearer"
        }

    raise HTTPException(status_code=400, detail="Missing login credentials")

@router.post("/refresh", response_model=TokenPair)
def refresh_token(token: str, db: Session = Depends(get_db)):
    """Refreshes the access token using a valid refresh token.

    Args:
        token (str): Refresh token to validate.
        db (Session): Database session dependency.

    Raises:
        HTTPException: If the refresh token is invalid.

    Returns:
        dict: New access and refresh tokens with token type.
    """
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user = crud_users.get_user_by_email(db, email)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        # Generate new access and refresh tokens
        access_token = auth.create_access_token(data={"sub": email})
        new_refresh_token = auth.create_refresh_token(data={"sub": email})
        return {
            "access_token": access_token, 
            "refresh_token": new_refresh_token, 
            "token_type": "bearer"
        }

    except JWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid refresh token") from exc

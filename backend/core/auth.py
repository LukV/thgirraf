import os
from pathlib import Path
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from firebase_admin import auth as firebase_auth
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

SECRET_KEY = os.getenv("SECRET_KEY").encode()
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # Default to HS256 if not set
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def hash_password(password: str) -> str:
    """Hashes a password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plaintext password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def verify_firebase_token(token: str) -> dict:
    """Verifies a Firebase token and returns the decoded data.
    
    Raises:
        HTTPException: If the token is invalid.
    """
    try:
        decoded_token = firebase_auth.verify_id_token(token)
        return decoded_token  # Contains 'uid', 'email', 'name', 'picture', etc.
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "AUTH_001",
                "message": "Invalid token."
            }
        ) from exc

def create_access_token(data: dict) -> str:
    """Creates an access JWT token.

    Args:
        data (dict): The data to encode in the JWT.

    Returns:
        str: The generated JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict) -> str:
    """Creates a refresh JWT token.

    Args:
        data (dict): The data to encode in the JWT.

    Returns:
        str: The generated refresh token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_password_reset_token(user_id: int) -> str:
    """
    Generate a password reset token for a given user ID.

    This function creates a JWT token that contains the user ID as a subject 
    and an expiration time set to 1 hour from the time of generation.
    """
    expires = datetime.now(timezone.utc) + timedelta(hours=1)  # Token expires in 1 hour
    to_encode = {"exp": expires, "sub": str(user_id)}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

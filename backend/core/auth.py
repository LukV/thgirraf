import os
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from firebase_admin import auth as firebase_auth
from fastapi import HTTPException, status
from jose import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # Default to HS256 if not set
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
            detail="Invalid Firebase token"
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

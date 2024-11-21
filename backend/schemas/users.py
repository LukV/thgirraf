from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, model_validator

class PasswordValidationMixin:
    """Mixin to add password validation logic."""

    @staticmethod
    def validate_password(password: str) -> str:
        """Validates that a password meets the required constraints."""
        if len(password) < 8 or len(password) > 128:
            raise ValueError("Password must be between 8 and 128 characters long.")
        if not any(c.isalpha() for c in password):
            raise ValueError("Password must include at least one letter.")
        if not any(c.isdigit() for c in password):
            raise ValueError("Password must include at least one number.")
        return password

class UserCreate(BaseModel, PasswordValidationMixin):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="The username for the new user. Must be unique."
    )
    email: EmailStr = Field(
        ...,
        description="The email address for the new user. Must be unique."
    )
    password: Optional[str] = Field(
        None,
        description=(
            "The password for the new user. Must be 8-128 characters long and include "
            "at least one letter and one number. Required unless using external authentication."
        )
    )
    icon: Optional[str] = Field(
        None,
        description="Optional URL of the user's profile icon or avatar."
    )

    @model_validator(mode="before")
    def validate_fields(cls, values): # pylint: disable=C0116, E0213
        password = values.get("password")
        if password:
            values['password'] = cls.validate_password(password)
        return values


class PasswordChange(BaseModel, PasswordValidationMixin):
    new_password: str = Field(
        ...,
        description=(
            "The new password for the user. Must be 8-128 characters long and include "
            "at least one letter and one number."
        )
    )

    @model_validator(mode="before")
    def validate_fields(cls, values): # pylint: disable=C0116, E0213
        values['new_password'] = cls.validate_password(values['new_password'])
        return values

class PasswordResetRequest(BaseModel):
    email: EmailStr = Field(
        ...,
        description="The email address associated with the user account."
    )


class PasswordReset(BaseModel, PasswordValidationMixin):
    email: EmailStr = Field(
        ...,
        description="The email address associated with the user account."
    )
    new_password: str = Field(
        ...,
        description=(
            "The new password for the user. Must be 8-128 characters long and include "
            "at least one letter and one number."
        )
    )
    token: str = Field(
        ...,
        description="The token sent to the user for verifying the password reset request."
    )

    @model_validator(mode="before")
    def validate_fields(cls, values): # pylint: disable=C0116, E0213
        values['new_password'] = cls.validate_password(values['new_password'])
        return values

class UserUpdate(BaseModel):
    username: Optional[str] = Field(
        None,
        min_length=3,
        max_length=50,
        description="The updated username. Must be unique."
    )
    email: Optional[EmailStr] = Field(
        None,
        description="The updated email address. Must be unique."
    )
    icon: Optional[str] = Field(
        None,
        description="Optional updated URL of the user's profile icon or avatar."
    )


class UserResponse(BaseModel):
    id: int = Field(
        ...,
        description="The unique identifier of the user."
    )
    uid: str = Field(
        ...,
        description="A unique public identifier for the user."
    )
    username: str = Field(
        ...,
        description="The username of the user."
    )
    email: EmailStr = Field(
        ...,
        description="The email address of the user."
    )
    icon: Optional[str] = Field(
        None,
        description="The URL of the user's profile icon or avatar, if available."
    )
    date_created: datetime = Field(
        ...,
        description="The timestamp when the user was created."
    )

    class Config:
        from_attributes = True

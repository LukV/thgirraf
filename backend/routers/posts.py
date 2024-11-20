from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas import posts as post_schemas
from ..db import models
from ..db.database import get_db
from ..crud import posts as crud_posts
from ..crud.users import get_current_user


router = APIRouter()

@router.post("/", response_model=post_schemas.PostResponse)
def create_post(
    post: post_schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Endpoint to create a new post. Authenticated users only.

    Args:
        post (PostCreate): The post creation schema.
        db (Session): Database session dependency.
        current_user (models.User): The authenticated user from JWT.

    Returns:
        PostResponse: The created post.
    """
    return crud_posts.create_post(db=db, post=post, user_id=current_user.id)


@router.get("/", response_model=List[post_schemas.PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    """
    Retrieve a list of all posts in the database.

    Returns:
        List[PostResponse]: A list of posts.
    """
    return crud_posts.get_all_posts(db)

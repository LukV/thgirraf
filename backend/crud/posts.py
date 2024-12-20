from typing import List
import logging
from fastapi import HTTPException, status
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
import ulid
from ..schemas import posts as post_schemas
from ..core.utils import extract_url_from_text, extract_metadata 
from ..db import models

logger = logging.getLogger(__name__)

def create_post(db: Session,
                post: post_schemas.PostCreate,
                user_id: int) -> models.Post:
    """
    Creates a new post in the database.

    Args:
        db (Session): The database session.
        post (PostCreate): The post creation schema.

    Returns:
        Post: The created post instance.
    """
    try:
        pid = str(ulid.new())

        # Extract URL and metadata
        url = extract_url_from_text(post.text)
        metadata = extract_metadata(url) if url else {}
        db_post = models.Post(
            pid=pid,
            text=post.text,
            user_id=user_id,
            title=metadata.get("title"),
            description=metadata.get("description"),
            image_url=metadata.get("image_url")
        )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    except SQLAlchemyError as exc:
        db.rollback()
        logger.error("Database error while creating post: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected database error occurred."
        ) from exc

def get_all_posts(db: Session) -> List[models.Post]:
    """
    Retrieves all posts from the database.

    Args:
        db (Session): The database session.

    Returns:
        List[Post]: A list of all post instances.
    """
    return db.query(models.Post).order_by(desc(models.Post.date_created)).all()

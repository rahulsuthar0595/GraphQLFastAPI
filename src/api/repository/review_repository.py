import logging
from typing import Annotated

import strawberry

from src.api.models.movie import Movie
from src.api.models.review import Review
from src.api.models.users import User

ReviewFilter = Annotated["ReviewFilter", strawberry.lazy("src.api.schemas.definitions")]

logging.basicConfig(level=logging.INFO)


async def fetch_all_movie_reviews_data(
    db,
    movie_id: int,
    page: int | None = None,
    page_size: int | None = None,
    filters: list | None = None,
):
    try:
        if not filters:
            filters = []

        base_query = (
            db.query(
                Review
                # Review.id, Review.user_id, Review.movie_id, Review.rating, Review.review_text,
                # Movie.title.label("movie_name"), User.email.label("user_email")
            )
            # .join(Movie, Review.movie_id == Movie.id)
            # .join(User, Review.user_id == User.id)
            .filter(Review.movie_id == movie_id)
        )
        for flt in filters:
            base_query = base_query.filter(flt)

        if page and page_size:
            skip = (page - 1) * page_size
            base_query = base_query.offset(skip).limit(page_size)

        reviews = base_query.all()
        return reviews
    except Exception as e:
        logging.error(f"Error in repository fetch_all_movie_reviews_data: {e}")
        raise e


async def fetch_all_movie_reviews_data_by_filter(
    db,
    movie_id: int,
    page: int | None = None,
    page_size: int | None = None,
    review_filter: ReviewFilter | None = None,
):
    try:
        filters = []
        if review_filter:
            if rating := review_filter.rating:
                filters.append(Review.rating == rating)
            if review_text := review_filter.review_text:
                # Case-insensitive search
                filters.append(Review.title.icontains(f"%{review_text}%"))

        reviews = await fetch_all_movie_reviews_data(
            db=db, movie_id=movie_id, page=page, page_size=page_size, filters=filters
        )
        return reviews
    except Exception as e:
        logging.error(
            f"Error in repository fetch_all_movie_reviews_data_by_filter: {e}"
        )
        raise e


async def fetch_review_by_id(db, review_id: int):
    try:
        query = (
            db.query(
                Review
                # Review, Movie.title.label("movie_name"), User.email.label("user_email")
            )
            # .join(Movie, Review.movie_id == Movie.id)
            # .join(User, Review.user_id == User.id)
            .filter(Review.id == review_id)
        )
        review = query.first()
        return review
    except Exception as e:
        logging.error(f"Error in repository fetch_review_by_id: {e}")
        raise e


async def create_review(db, data: dict):
    try:
        new_review = Review(**data)
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        return new_review
    except Exception as e:
        logging.error(f"Error in repository create_review: {e}")
        raise e


async def update_review(db, review, data: dict):
    try:
        for key, value in data.items():
            setattr(review, key, value)

        db.commit()
        db.refresh(review)
        return review
    except Exception as e:
        logging.error(f"Error in repository update_review: {e}")
        raise e


async def delete_review(db, review):
    try:
        db.delete(review)
        db.commit()
        db.refresh()
    except Exception as e:
        logging.error(f"Error in repository delete_review: {e}")
        raise e

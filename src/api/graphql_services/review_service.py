import logging
from typing import TYPE_CHECKING, Annotated, List

import strawberry
from graphql import GraphQLError

from src.api.models.review import Review
from src.api.repository.review_repository import (
    delete_review,
    fetch_all_movie_reviews_data,
    fetch_all_movie_reviews_data_by_filter,
    fetch_review_by_id,
    update_review,
)

if TYPE_CHECKING:
    from src.api.schemas.definitions import ReviewFilter, ReviewInput, ReviewType

logging.basicConfig(level=logging.INFO)


async def get_all_reviews_data_for_movie(
    db, movie_id: int, page: int | None = None, page_size: int | None = None
) -> (
    List[Annotated["ReviewType", strawberry.lazy("src.api.schemas.definitions")]] | None
):
    from src.api.schemas.definitions import ReviewType

    try:
        reviews = await fetch_all_movie_reviews_data(
            db=db, movie_id=movie_id, page_size=page_size, page=page, filters=[]
        )
        return list(map(lambda review: ReviewType(**review.__dict__), reviews))
    except Exception as e:
        logging.error(f"Error in get_all_reviews_data_for_movie: {e}")
        raise GraphQLError(message="Something went wrong")


async def get_review_data_by_id(
    db, review_id: int
) -> Annotated["ReviewType", strawberry.lazy("src.api.schemas.definitions")] | None:
    try:
        review = await fetch_review_by_id(db=db, review_id=review_id)
        return ReviewType(**review.__dict__)
    except Exception as e:
        logging.error(f"Error in get_review_data_by_id: {e}")
        raise GraphQLError(message="Something went wrong")


async def get_review_data_by_filters(
    db,
    movie_id: int,
    page: int | None = None,
    page_size: int | None = None,
    review_filter: (
        Annotated["ReviewFilter", strawberry.lazy("src.api.schemas.definitions")] | None
    ) = None,
) -> (
    List[Annotated["ReviewType", strawberry.lazy("src.api.schemas.definitions")]] | None
):
    try:
        reviews = await fetch_all_movie_reviews_data_by_filter(
            db=db,
            movie_id=movie_id,
            page=page,
            page_size=page_size,
            review_filter=review_filter,
        )
        return list(map(lambda review: ReviewType(**review.__dict__), reviews))
    except Exception as e:
        logging.error(f"Error in get_review_data_by_filters: {e}")
        raise GraphQLError(message="Something went wrong")


async def create_review_data(
    db, data: Annotated["ReviewInput", strawberry.lazy("src.api.schemas.definitions")]
) -> Annotated["ReviewType", strawberry.lazy("src.api.schemas.definitions")]:
    from src.api.repository.movie_repository import create_movie

    try:
        review_filter = [
            Review.movie_id == data.movie_id,
            Review.user_id == data.user_id,
        ]
        existing_review = await fetch_all_movie_reviews_data(
            db=db, movie_id=data.movie_id, page=1, page_size=1, filters=review_filter
        )
        if existing_review:
            raise GraphQLError(message="Review Already Exist For Movie")

        data = data.__dict__
        new_review = await create_movie(db=db, data=data)
        return ReviewType(**new_review.__dict__)
    except GraphQLError as gql_err:
        raise gql_err
    except Exception as e:
        logging.error(f"Error in create_review_data: {e}")
        raise GraphQLError(message="Something went wrong")


async def update_review_data(
    db,
    review_id: int,
    data: Annotated["ReviewInput", strawberry.lazy("src.api.schemas.definitions")],
) -> Annotated["ReviewType", strawberry.lazy("src.api.schemas.definitions")]:
    try:
        review = await fetch_review_by_id(db=db, review_id=review_id)
        if not review:
            raise GraphQLError(message="Record not found")

        if review.movie_id != data.movie_id or review.user_id != data.user_id:
            raise GraphQLError(message="Cannot change user and movie field")

        if review.rating > 5:
            raise GraphQLError(message="Rating should be between 1 to 5.")

        new_data = data.__dict__
        updated_review = await update_review(db=db, review=review, data=new_data)
        return ReviewType(**updated_review.__dict__)
    except GraphQLError as gql_err:
        raise gql_err
    except Exception as e:
        logging.error(f"Error in update_review_data: {e}")
        raise GraphQLError(message="Something went wrong")


async def delete_review_data(db, review_id: int) -> bool:
    try:

        review = await fetch_review_by_id(db=db, review_id=review_id)
        if not review:
            raise GraphQLError(message="Record not found")

        await delete_review(db=db, review=review)
        return True
    except GraphQLError as gql_err:
        raise gql_err
    except Exception as e:
        logging.error(f"Error in delete_review_data: {e}")
        raise GraphQLError(message="Something went wrong")

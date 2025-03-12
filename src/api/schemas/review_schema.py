import logging
from typing import List, Optional

import strawberry

from src.api.graphql_services.review_service import (
    create_review_data,
    delete_review_data,
    get_all_reviews_data_for_movie,
    get_review_data_by_id,
    update_review_data,
)
from src.api.repository.review_repository import fetch_all_movie_reviews_data_by_filter
from src.api.schemas.definitions import MovieType, ReviewFilter, ReviewInput, ReviewType

logging.basicConfig(level=logging.INFO)


@strawberry.type
class ReviewQuery:

    @strawberry.field()
    async def get_movie_reviews(
        self, info: strawberry.Info, movie_id: int, page: int, page_size: int
    ) -> List[ReviewType]:
        db = info.context["db"]
        return await get_all_reviews_data_for_movie(
            db=db, movie_id=movie_id, page=page, page_size=page_size
        )

    @strawberry.field()
    async def get_review_by_id(
        self,
        info: strawberry.Info,
        review_id: int,
    ) -> MovieType | None:
        db = info.context["db"]
        return await get_review_data_by_id(db=db, review_id=review_id)

    @strawberry.field(
        deprecation_reason="In Future, this endpoint will be merged with 'getMovieReviews' endpoint."
    )
    async def get_movie_reviews_by_filter(
        self,
        info: strawberry.Info,
        movie_id: int,
        page: int,
        page_size: int,
        review_filter: Optional[ReviewFilter] = None,
    ) -> List[MovieType]:
        db = info.context["db"]
        return await fetch_all_movie_reviews_data_by_filter(
            db=db,
            movie_id=movie_id,
            page=page,
            page_size=page_size,
            review_filter=review_filter,
        )


@strawberry.type
class ReviewMutation:

    @strawberry.mutation()
    async def create_review(
        self, info: strawberry.Info, data: ReviewInput
    ) -> ReviewType:
        db = info.context["db"]
        return await create_review_data(db=db, data=data)

    @strawberry.mutation()
    async def update_review(
        self, info: strawberry.Info, review_id: int, data: ReviewInput
    ) -> ReviewType:
        db = info.context["db"]
        return await update_review_data(db=db, review_id=review_id, data=data)

    @strawberry.mutation()
    async def delete_review(self, info: strawberry.Info, review_id: int) -> bool:
        db = info.context["db"]
        return await delete_review_data(db=db, review_id=review_id)

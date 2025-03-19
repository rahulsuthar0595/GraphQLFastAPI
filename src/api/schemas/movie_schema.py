import logging
from typing import List, Optional

import strawberry

from src.api.graphql_services.movie_service import (
    create_movie_data,
    delete_movie_data,
    get_all_movies_data,
    get_movie_data_by_filters,
    get_movie_data_by_id,
    update_movie_data,
)
from src.api.schemas.definitions import MovieFilter, MovieInput, MovieType
from src.api.utils.permissions import IsAuthenticated

logging.basicConfig(level=logging.INFO)


@strawberry.type
class MovieQuery:

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def get_all_movies(
            self, info: strawberry.Info, page: int, page_size: int
    ) -> List[MovieType]:
        db = info.context["db"]
        return await get_all_movies_data(db=db, page=page, page_size=page_size)

    @strawberry.field()
    async def get_movie_by_id(
            self, movie_id: int, info: strawberry.Info
    ) -> MovieType | None:
        db = info.context["db"]
        return await get_movie_data_by_id(db=db, movie_id=movie_id)

    @strawberry.field(
        deprecation_reason="In Future, this endpoint will be merged with 'getAllMovies' endpoint."
    )
    async def get_movies_by_filter(
            self,
            info: strawberry.Info,
            page: int,
            page_size: int,
            movie_filter: Optional[MovieFilter] = None,
    ) -> List[MovieType]:
        db = info.context["db"]
        return await get_movie_data_by_filters(
            db=db, page=page, page_size=page_size, movie_filter=movie_filter
        )


@strawberry.type
class MovieMutation:

    @strawberry.mutation()
    async def create_movie(self, info: strawberry.Info, data: MovieInput) -> MovieType:
        db = info.context["db"]
        return await create_movie_data(db=db, data=data)

    @strawberry.mutation()
    async def update_movie(
            self, info: strawberry.Info, movie_id: int, data: MovieInput
    ) -> MovieType:
        db = info.context["db"]
        return await update_movie_data(db=db, movie_id=movie_id, data=data)

    @strawberry.mutation()
    async def delete_movie(self, info: strawberry.Info, movie_id: int) -> bool:
        db = info.context["db"]
        return await delete_movie_data(db=db, movie_id=movie_id)

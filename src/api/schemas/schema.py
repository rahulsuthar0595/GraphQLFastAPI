from typing import List, Optional

import strawberry
from sqlalchemy.inspection import inspect

from src.api.models.movie import Movie
from src.api.schemas.definitions import MovieType, MovieFilter


@strawberry.type
class MovieQuery:

    @strawberry.field()
    def get_all_movies(self, info: strawberry.Info) -> List[MovieType]:
        db = info.context["db"]
        limit = 10
        result = db.query(Movie).limit(limit).all()
        movies_data = [
            MovieType(**{c.key: getattr(movie, c.key) for c in inspect(movie).mapper.column_attrs}) for movie
            in result
        ]
        return movies_data

    @strawberry.field()
    def get_movie_by_id(self, movie_id: int, info: strawberry.Info) -> Optional[MovieType]:
        db = info.context["db"]
        result = db.query(Movie).filter(Movie.id == movie_id).first()
        if result:
            movie_data = {c.key: getattr(result, c.key) for c in inspect(result).mapper.column_attrs}
            return MovieType(**movie_data)
        return None

    @strawberry.field()
    def get_movies_by_filter(self, info: strawberry.Info, filter: Optional[MovieFilter] = None) -> List[MovieType]:
        db = info.context["db"]
        query = db.query(Movie)

        if filter:
            if filter.title:
                query = query.filter(Movie.title.ilike(f"%{filter.title}%"))  # Case-insensitive search
            if filter.genre:
                query = query.filter(Movie.genre == filter.genre)
            if filter.release_year:
                query = query.filter(Movie.release_year == filter.release_year)

        result = query.all()
        movies_data = [
            MovieType(**{c.key: getattr(movie, c.key) for c in inspect(movie).mapper.column_attrs}) for movie
            in result
        ]
        return movies_data


@strawberry.type
class Query(MovieQuery):
    pass

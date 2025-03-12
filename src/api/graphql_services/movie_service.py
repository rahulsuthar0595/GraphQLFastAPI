import logging
from typing import List

from graphql import GraphQLError
from sqlalchemy import func

from src.api.models.movie import Movie
from src.api.repository.movie_repository import (
    create_movie,
    delete_movie,
    fetch_all_movies_data,
    fetch_movie_by_id,
    fetch_movies_by_filter,
    update_movie,
)
from src.api.schemas.definitions import MovieFilter, MovieInput, MovieType

logging.basicConfig(level=logging.INFO)


async def get_all_movies_data(db, page: int, page_size: int) -> List[MovieType] | None:
    try:
        movies = await fetch_all_movies_data(
            db=db, page_size=page_size, page=page, filters=[]
        )
        return list(map(lambda movie: MovieType(**movie.__dict__), movies))
    except Exception as e:
        logging.error(f"Error in get_all_movies_data: {e}")
        raise GraphQLError(message="Something went wrong")


async def get_movie_data_by_id(db, movie_id: int) -> MovieType | None:
    try:
        movie = await fetch_movie_by_id(db=db, movie_id=movie_id)
        return MovieType(**movie.__dict__)
    except Exception as e:
        logging.error(f"Error in get_movie_data_by_id: {e}")
        raise GraphQLError(message="Something went wrong")


async def get_movie_data_by_filters(
    db, page: int, page_size: int, movie_filter: MovieFilter | None
) -> List[MovieType] | None:
    try:
        movies = await fetch_movies_by_filter(
            db=db, page=page, page_size=page_size, movie_filter=movie_filter
        )
        return list(map(lambda movie: MovieType(**movie.__dict__), movies))
    except Exception as e:
        logging.error(f"Error in get_movie_data_by_filters: {e}")
        raise GraphQLError(message="Something went wrong")


async def create_movie_data(db, data: MovieInput) -> MovieType:
    try:
        movie_filter = [
            func.lower(Movie.title) == data.title.strip().lower(),
            Movie.release_year == data.release_year,
        ]
        existing_movies = await fetch_all_movies_data(
            db=db, page=1, page_size=1, filters=movie_filter
        )
        if existing_movies:
            raise GraphQLError(message="Duplicate Record.")

        image = data.image.filename
        data = data.__dict__
        data["image"] = image
        new_movie = await create_movie(db=db, data=data)
        return MovieType(**new_movie.__dict__)
    except GraphQLError as gql_err:
        raise gql_err
    except Exception as e:
        logging.error(f"Error in create_movie_data: {e}")
        raise GraphQLError(message="Something went wrong")


async def update_movie_data(db, movie_id: int, data: MovieInput) -> MovieType:
    try:
        movie = await fetch_movie_by_id(db=db, movie_id=movie_id)
        if not movie:
            raise GraphQLError(message="Record not found")

        movie_filter = [
            Movie.id != movie_id,
            func.lower(Movie.title) == data.title.strip().lower(),
            Movie.release_year == data.release_year,
        ]
        existing_movies = await fetch_all_movies_data(
            db=db, page=1, page_size=1, filters=movie_filter
        )
        if existing_movies:
            raise GraphQLError(message="Duplicate Record.")

        image = data.image.filename
        new_data = data.__dict__
        new_data["image"] = image
        updated_movie = await update_movie(db=db, movie=movie, data=new_data)
        return MovieType(**updated_movie.__dict__)
    except GraphQLError as gql_err:
        raise gql_err
    except Exception as e:
        logging.error(f"Error in update_movie_data: {e}")
        raise GraphQLError(message="Something went wrong")


async def delete_movie_data(db, movie_id: int) -> bool:
    try:

        movie = await fetch_movie_by_id(db=db, movie_id=movie_id)
        if not movie:
            raise GraphQLError(message="Record not found")

        await delete_movie(db=db, movie=movie)
        return True
    except GraphQLError as gql_err:
        raise gql_err
    except Exception as e:
        logging.error(f"Error in delete_movie_data: {e}")
        raise GraphQLError(message="Something went wrong")

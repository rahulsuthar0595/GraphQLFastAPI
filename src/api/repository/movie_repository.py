import logging

from src.api.models.movie import Movie
from src.api.schemas.definitions import MovieFilter

logging.basicConfig(level=logging.INFO)


async def fetch_all_movies_data(
    db, page: int, page_size: int, filters: list | None = None
):
    try:
        base_query = db.query(Movie)
        if not filters:
            filters = []

        for flt in filters:
            base_query = base_query.filter(flt)

        skip = (page - 1) * page_size
        movies = base_query.offset(skip).limit(page_size).all()
        return movies
    except Exception as e:
        logging.error(f"Error in repository fetch_all_movies_data: {e}")
        raise e


async def fetch_movie_by_id(db, movie_id: int):
    try:
        movie = db.query(Movie).filter(Movie.id == movie_id).first()
        return movie
    except Exception as e:
        logging.error(f"Error in repository fetch_movie_by_id: {e}")
        raise e


async def fetch_movies_by_filter(
    db, page: int, page_size: int, movie_filter: MovieFilter | None
):
    try:
        filters = []
        if movie_filter:
            if movie_filter.title:
                filters.append(
                    Movie.title.ilike(f"%{movie_filter.title}%")
                )  # Case-insensitive search
            if movie_filter.genre:
                filters.append(Movie.genre == movie_filter.genre)
            if movie_filter.release_year:
                filters.append(Movie.release_year == movie_filter.release_year)

        movies = await fetch_all_movies_data(
            db=db, page=page, page_size=page_size, filters=filters
        )
        return movies
    except Exception as e:
        logging.error(f"Error in repository fetch_movies_by_filter: {e}")
        raise e


async def create_movie(db, data: dict):
    try:
        new_movie = Movie(**data)
        db.add(new_movie)
        db.commit()
        db.refresh(new_movie)
        return new_movie
    except Exception as e:
        logging.error(f"Error in repository create_movie: {e}")
        raise e


async def update_movie(db, movie, data: dict):
    try:
        for key, value in data.items():
            setattr(movie, key, value)

        db.commit()
        db.refresh(movie)
        return movie
    except Exception as e:
        logging.error(f"Error in repository update_movie: {e}")
        raise e


async def delete_movie(db, movie):
    try:
        db.delete(movie)
        db.commit()
        db.refresh()
    except Exception as e:
        logging.error(f"Error in repository update_movie: {e}")
        raise e

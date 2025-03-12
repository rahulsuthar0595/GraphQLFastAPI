from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from database.db_connection import get_db
from src.api.repository.movie_repository import fetch_all_movies_data
from src.api.repository.review_repository import fetch_all_movie_reviews_data
from src.api.schemas.definitions import MovieSchema

router = APIRouter(prefix="/movies")


@router.get(
    "/list",
    summary="Get Movies List",
    status_code=status.HTTP_200_OK,
    response_model=List[MovieSchema],
)
async def get_movies_list(
    page: int, page_size: int = 10, db: Session = Depends(get_db)
):
    try:
        movies = await fetch_all_movies_data(
            db=db, page_size=page_size, page=page, filters=[]
        )
        for movie in movies:
            movie.reviews = await fetch_all_movie_reviews_data(db=db, movie_id=movie.id)
        return movies
    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=HTTPStatus.BAD_REQUEST)

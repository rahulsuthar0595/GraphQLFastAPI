from dataclasses import dataclass

import strawberry


@dataclass
class BaseMovieCls:
    id: int
    title: str
    description: str
    release_year: int
    genre: str
    image: str | None


@strawberry.type
class MovieType(BaseMovieCls):
    pass


@strawberry.input
class MovieInput(BaseMovieCls):
    pass


@strawberry.input
class MovieFilter:
    id: int | None = None
    title: str | None = None
    description: str | None = None
    release_year: int | None = None
    genre: str | None = None


@strawberry.mutation
def add_movie(input: MovieInput) -> MovieType:
    # Implement movie creation logic
    pass

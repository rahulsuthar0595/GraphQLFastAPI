from dataclasses import dataclass, fields
from enum import Enum
from typing import List, Optional

import strawberry
from pydantic import BaseModel
from strawberry.file_uploads import Upload

from src.api.graphql_services.review_service import get_all_reviews_data_for_movie


@dataclass
class FilteredDataMixin:
    def __init__(self, **kwargs):
        allowed_keys = {f.name for f in fields(self)}
        self.__dict__.update({k: v for k, v in kwargs.items() if k in allowed_keys})


@strawberry.type
class ReviewType(FilteredDataMixin):
    id: int
    user_id: int
    movie_id: int
    rating: int
    review_text: str | None = None

    # user_email: str | None = None
    # movie_name: str | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@strawberry.input
class ReviewInput(FilteredDataMixin):
    user_id: int
    movie_id: int
    rating: int
    review_text: str | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@strawberry.input
class ReviewFilter(FilteredDataMixin):
    rating: int | None
    review_text: str | None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

from strawberry.schema_directive import Location


@strawberry.schema_directive(locations=[val for val in Location])
class Keys:
    title: str


@strawberry.type(directives=[Keys(title="title")])
class MovieType(FilteredDataMixin):
    id: int
    title: str
    description: str
    release_year: int
    genre: str
    image: str | None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @strawberry.field()
    async def reviews(self, parent: strawberry.Parent, info: strawberry.Info) -> List[ReviewType]:
        db = info.context["db"]
        return await get_all_reviews_data_for_movie(db=db, movie_id=self.id)

    # @strawberry.field()
    # async def reviews(self, info: strawberry.Info) -> List[ReviewType]:
    #     # NOTE: Enable for Data Loader
    #     loader = info.context["review_dataloader"]
    #     res = await loader.load(self.id)
    #     return res


@strawberry.input
class MovieFilter(FilteredDataMixin):
    id: int | None = None
    title: str | None = None
    description: str | None = None
    release_year: int | None = None
    genre: str | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@strawberry.input
class MovieInput:
    title: str
    description: str
    release_year: int
    genre: str
    image: Optional[Upload] = None


@strawberry.enum
class UserRoleEnum(Enum):
    ADMIN = "admin"
    USER = "user"


@strawberry.input
class UserRegister:
    email: str
    password: str
    role: UserRoleEnum


@strawberry.input
class UserLogin:
    email: str
    password: str


@strawberry.type
class UserError:
    message: str
    status_code: int


@strawberry.type
class UserType(FilteredDataMixin):
    id: int
    email: str
    hashed_password: strawberry.Private[str]
    role: UserRoleEnum

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ReviewSchema(BaseModel):
    id: int
    user_id: int
    movie_id: int
    rating: int
    review_text: Optional[str]

    class Config:
        from_attributes = True


class MovieSchema(BaseModel):
    id: int
    title: str
    genre: str
    release_year: int
    reviews: List[ReviewSchema] = []

    class Config:
        from_attributes = True

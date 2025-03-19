from http import HTTPStatus
from typing import Annotated, Union, Optional

import strawberry

from src.api.graphql_services.user_service import fetch_user_by_email, user_register, validate_user_login
from src.api.schemas.definitions import UserRegister, UserType, UserLogin, UserError

UserLoginResult = Annotated[
    Union[UserType, UserError], strawberry.union("UserLoginResult")
]


@strawberry.type
class UserQuery:

    @strawberry.field()
    async def get_user_by_email(
            self, info: strawberry.Info, email: str
    ) -> UserType | None:
        db = info.context["db"]
        return await fetch_user_by_email(db=db, email=email)


@strawberry.type
class UserMutation:

    @strawberry.mutation()
    async def register_user(
            self, info: strawberry.Info, form: UserRegister
    ) -> UserType | None:
        db = info.context["db"]
        return await user_register(
            db=db, email=form.email, password=form.password, role=form.role.value
        )

    @strawberry.mutation()
    async def login_user(self, info: strawberry.Info, form: UserLogin) -> Optional[UserLoginResult]:
        db = info.context["db"]
        status, message, user = await validate_user_login(db=db, email=form.email, password=form.password)
        if not status:
            return UserError(message=message, status_code=HTTPStatus.BAD_REQUEST)
        return UserType(**user.__dict__)

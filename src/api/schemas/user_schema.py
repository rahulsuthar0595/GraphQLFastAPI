import strawberry

from src.api.graphql_services.user_service import fetch_user_by_email, user_register
from src.api.schemas.definitions import UserRegister, UserType


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

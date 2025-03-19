import typing

from strawberry import Info
from strawberry.exceptions import StrawberryGraphQLError
from strawberry.permission import BasePermission


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"
    error_class = StrawberryGraphQLError
    error_extensions = {"code": "UNAUTHORIZED"}

    def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        return True

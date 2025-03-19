from enum import Enum
from typing import List

import strawberry
from strawberry.schema_directive import Location


@strawberry.enum
class RoleEnum(Enum):
    ADMIN = "admin"
    USER = "user"


@strawberry.schema_directive(locations=[Location.OBJECT], print_definition=True)
class Auth:
    role: RoleEnum

    def __init__(self, role):
        self.role = role


@strawberry.federation.type(keys=["id"], )
class Book:
    id: strawberry.ID
    title: str


def get_all_books() -> List[Book]:
    return [Book(id=strawberry.ID("1"), title="The Dark Tower")]


@strawberry.type
class Query:
    all_books: List[Book] = strawberry.field(resolver=get_all_books)


schema = strawberry.federation.Schema(query=Query, enable_federation_2=True, schema_directives=[Auth])

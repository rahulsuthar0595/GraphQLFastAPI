import time
from typing import List

import strawberry


@strawberry.type
class Review:
    id: int
    body: str


def get_reviews(root: "Book") -> List[Review]:
    time.sleep(1)
    return [
        Review(id=id_, body=f"A review for {root.id}")
        for id_ in range(3)
    ]


@strawberry.federation.type(keys=["id"])
class Book:
    id: strawberry.ID
    reviews: List[Review] = strawberry.field(resolver=get_reviews)


@strawberry.type
class Query:
    _hi: str = strawberry.field(resolver=lambda: "Hello World!")


schema = strawberry.federation.Schema(
    query=Query, types=[Book, Review], enable_federation_2=True
)

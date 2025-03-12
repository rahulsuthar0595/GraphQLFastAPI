import strawberry

from .movie_schema import MovieMutation, MovieQuery
from .review_schema import ReviewMutation, ReviewQuery
from .subscription import TestingSubscription
from .user_schema import UserMutation, UserQuery


@strawberry.type
class Query(MovieQuery, UserQuery, ReviewQuery):
    pass


@strawberry.type
class Mutation(MovieMutation, UserMutation, ReviewMutation):
    pass


@strawberry.type
class Subscription(TestingSubscription):
    pass
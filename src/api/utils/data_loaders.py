from collections import defaultdict
from typing import List

from strawberry.dataloader import DataLoader

from src.api.models.review import Review


async def batch_load_reviews(db, movie_ids) -> List[List[Review]]:
    base_query = (
        db.query(Review)
        .filter(Review.movie_id.in_(movie_ids))
    )
    reviews = base_query.all()
    # Group reviews by movie_id
    reviews_map = defaultdict(list)
    for review in reviews:
        reviews_map[review.movie_id].append(review)
    return [reviews_map[movie_id] for movie_id in movie_ids]


async def get_review_loader(db):
    return DataLoader(load_fn=lambda movie_ids: batch_load_reviews(db, movie_ids))

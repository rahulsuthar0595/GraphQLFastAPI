from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from strawberry import Schema

from config.config import settings
from database.db_connection import get_db
from src.api.schemas.base_schema import Mutation, Query, Subscription
from src.api.utils.data_loaders import get_review_loader
from src.api.utils.directives import to_title_case
from src.api.utils.extensions import ResponseLogExtension
from src.api.utils.graphql_router import CustomGraphQLRouter
from src.api.views import movies_views


async def extra_context_dependency(db: Session = Depends(get_db)):
    return {"db": db, "review_dataloader": await get_review_loader(db)}


schema = Schema(query=Query, mutation=Mutation, subscription=Subscription, extensions=[ResponseLogExtension],
                directives=[to_title_case])

graphql_router = CustomGraphQLRouter(
    schema=schema,
    graphql_ide=settings.GRAPHQL_IDE,
    context_getter=extra_context_dependency,
    multipart_uploads_enabled=True,
)

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(movies_views.router, tags=["Movies API"])

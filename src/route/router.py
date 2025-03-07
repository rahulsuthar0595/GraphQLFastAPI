from fastapi import Depends
from sqlalchemy.orm import Session
from strawberry import Schema
from strawberry.fastapi import GraphQLRouter

from config.config import settings
from database.db_connection import get_db
from src.api.schemas.schema import Query


async def custom_context_dependency(db: Session = Depends(get_db)):
    return {"db": db}


schema = Schema(query=Query)

graphql_router = GraphQLRouter(
    schema=schema, graphql_ide=settings.GRAPHQL_IDE,
    context_getter=custom_context_dependency
)

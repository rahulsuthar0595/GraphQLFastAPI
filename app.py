from fastapi import FastAPI

from src.api.utils.middleware import ResponseLogMiddleware
from src.route.router import api_router, graphql_router

app = FastAPI()
app.include_router(graphql_router, prefix="/graphql")
app.include_router(api_router)

app.add_middleware(ResponseLogMiddleware)


@app.get("/", summary="Default Endpoint for Service")
async def index():
    return {"success": True, "message": "Success"}

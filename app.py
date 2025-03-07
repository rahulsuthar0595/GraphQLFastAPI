from fastapi import FastAPI

from src.route.router import graphql_router

app = FastAPI()
app.include_router(graphql_router, prefix="/graphql")


@app.get("/", summary="Default Endpoint for Service")
async def index():
    return {"success": True, "message": "Success"}

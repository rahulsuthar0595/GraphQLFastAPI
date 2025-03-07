import uvicorn
from config.config import settings

if __name__ == "__main__":
    uvicorn.run(app="app:app", host="0.0.0.0", port=8002, reload=settings.DEBUG)

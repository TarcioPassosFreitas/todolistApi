from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from configs.environment import get_environment_variables
from repositories.models import init as init_db
from routers.task_router import router as task_router

env = get_environment_variables()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=env.APP_NAME,
    version=env.API_VERSION,
    lifespan=lifespan
)

app.include_router(task_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)

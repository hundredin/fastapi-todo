from fastapi import FastAPI

from api.routers import task
from api.routers import done
app = FastAPI()


app.include_router(task.router)
app.include_router(done.router)
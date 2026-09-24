from fastapi import FastAPI

from .config import settings
from .database import Base, engine
from .routers import auth, tasks, users

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, version="0.1.0")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)


@app.get("/", tags=["health"])
def root():
    return {"message": f"{settings.APP_NAME} is running. See /docs for API."}


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}

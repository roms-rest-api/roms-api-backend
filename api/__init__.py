from fastapi import FastAPI
from .routers import main

app = FastAPI()

app.include_router(
    router=main.main_router
)

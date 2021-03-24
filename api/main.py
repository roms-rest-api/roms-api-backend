from . import app
from .routers import main as main_route, changelog

def main():
    app.include_router(router=main_route.router)
    app.include_router(router=changelog.router)

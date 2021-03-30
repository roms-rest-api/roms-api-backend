from . import app
from .routers import main as main_route, changelog, upload_to_gdrive, auth


def main():
    app.include_router(router=main_route.router)
    app.include_router(router=changelog.router)
    app.include_router(router=upload_to_gdrive.router)
    app.include_router(router=auth.router)

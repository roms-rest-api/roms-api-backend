from . import app
from .routers import main as main_route, changelog, upload_to_gdrive, frontend

from fastapi.middleware.cors import CORSMiddleware

def main():
    app.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
    )

    app.include_router(router=main_route.router)
    app.include_router(router=changelog.router)
    app.include_router(router=upload_to_gdrive.router)
    app.include_router(router=frontend.router)

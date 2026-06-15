from __future__ import annotations
from fastapi import FastAPI

from .config.settings import settings
from .database import init_db
from .grievance_assistant.backend.routes import config as config_routes
from .grievance_assistant.backend.routes import grievances as grievances_routes
from .grievance_assistant.backend.routes import reports as reports_routes


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, debug=settings.debug)

    @app.on_event("startup")
    def _startup() -> None:
        init_db()

    app.include_router(config_routes.router)
    app.include_router(grievances_routes.router)
    app.include_router(reports_routes.router)

    return app


app = create_app()

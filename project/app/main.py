import logging
import os

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.api import home, ping, sentiments
from app.db import init_db

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    fullPath = os.path.dirname(__file__) + "/static"
    log.info(f"Mounting static files at: {fullPath}")
    application.mount(fullPath, StaticFiles(directory=fullPath), name="static")
    application.include_router(ping.router)
    application.include_router(home.router)
    application.include_router(
        sentiments.router, prefix="/sentiments", tags=["sentiments"]
    )
    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")

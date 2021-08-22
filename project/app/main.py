from fastapi import FastAPI
import logging
from app.api import ping, sentiments, home
from app.db import init_db
from starlette.staticfiles import StaticFiles
import os

log = logging.getLogger('uvicorn')

def create_application() -> FastAPI:
    application = FastAPI()
    fullPath = os.environ.get("STATIC_PATH")
    log.info(f"Mounting static files at: {fullPath}")
    application.mount(fullPath, StaticFiles(directory=fullPath), name="static")
    application.include_router(ping.router)
    application.include_router(home.router)
    application.include_router(sentiments.router, prefix="/sentiments", tags=["sentiments"])
    return application

app = create_application()

@app.on_event('startup')
async def startup_event():
    log.info('Starting up...')
    init_db(app)
    
@app.on_event('shutdown')
async def shutdown_event():
    log.info('Shutting down...')
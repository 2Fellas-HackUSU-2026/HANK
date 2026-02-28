from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from API.routes import backend_routes
from API.routes import frontend_routes

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(frontend_routes.router)
app.include_router(backend_routes.router)
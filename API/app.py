from fastapi import FastAPI
from API.routes import backend_routes

app = FastAPI()


app.include_router(backend_routes.router)

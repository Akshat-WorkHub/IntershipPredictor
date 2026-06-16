from fastapi import FastAPI
from src.api.routers.user_profile import router

app = FastAPI(
    title="Internship Predictor API"
)

app.include_router(router)
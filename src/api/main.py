from fastapi import FastAPI
from src.api.routers.user_profile import router as profile_router
from src.api.routers.roadmap import router as roadmap_router
from src.api.routers.interview import router as interview_router

app = FastAPI(
    title="Internship Predictor API"
)

app.include_router(profile_router)
app.include_router(roadmap_router)
app.include_router(interview_router)
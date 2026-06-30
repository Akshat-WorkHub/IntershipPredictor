from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from src.api.routers.user_profile import router as profile_router
from src.api.routers.roadmap import router as roadmap_router
from src.api.routers.interview import router as interview_router
from src.api.routers.interview_preparation import router as interview_preparation_router
from src.api.routers.pdf_download import router as pdf_download_router



app = FastAPI(
    title="Internship Predictor API"
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profile_router)
app.include_router(roadmap_router)
app.include_router(interview_router)
app.include_router(interview_preparation_router)
app.include_router(pdf_download_router)

frontend_dir = Path(__file__).resolve().parents[1] / "frontend"
app.mount(
    "/",
    StaticFiles(directory=frontend_dir, html=True),
    name="frontend"
)


from fastapi import APIRouter

from src.parsers.pydantic_models import RoadmapRequest
from src.services.learning_roadmap_service import LearningRoadmapService

router = APIRouter(prefix="/roadmap", tags=["Roadmap"])

@router.post("/generate")
async def generate_roadmap(request: RoadmapRequest):

    roadmap_service = LearningRoadmapService()

    roadmap = roadmap_service.generate_roadmap(
        request.missing_skills
    )

    return roadmap

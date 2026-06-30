from fastapi import APIRouter
from src.services.interview_preparation_service import InterviewPreparationService
from src.parsers.pydantic_models import InterviewRequest

router = APIRouter(
    prefix="/interview-preparation",
    tags=["Interview Preparation"]
)

@router.post("/generate")
async def generate_interview_preparation(
    request: InterviewRequest
):

    service = InterviewPreparationService()

    return service.generate(
        interview_mode=request.interview_mode,
        difficulty=request.difficulty,
        number_of_questions=request.number_of_questions,
        resume_data=request.resume_data,
        jd_data=request.jd_data,
        missing_skills=request.missing_skills
    )
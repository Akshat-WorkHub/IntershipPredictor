from fastapi import APIRouter

from src.parsers.pydantic_models import InterviewRequest
from src.services.interview_service import InterviewService

router = APIRouter(prefix="/interview", tags=["Interview"])

@router.post("/generate")
async def generate_interview_questions(
    request: InterviewRequest
):

    interview_service = InterviewService()

    result = (
        interview_service.generate_questions(
            interview_mode=request.interview_mode,
            number_of_questions=request.number_of_questions,
            resume_data=request.resume_data.model_dump(),
            jd_data=request.jd_data.model_dump(),
            missing_skills=request.missing_skills
        )
    )

    return result
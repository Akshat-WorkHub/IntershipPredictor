from io import BytesIO

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src.services.pdf_service import (
    InterviewPreparationPDFService
)

from src.parsers.pydantic_models import (
    InterviewPreparationPDFRequest
)


router = APIRouter(
    prefix="/interview-preparation",
    tags=["Interview Preparation"]
)


@router.post("/download")
async def download_interview_preparation(
    request: InterviewPreparationPDFRequest
):

    pdf_service = InterviewPreparationPDFService()

    pdf = pdf_service.generate_pdf(
        interview_mode=request.interview_mode,
        difficulty=request.difficulty,
        questions=request.questions
    )

    return StreamingResponse(
        BytesIO(pdf),
        media_type="application/pdf",
        headers={
            "Content-Disposition":
            "attachment; filename=Interview_Preparation_Guide.pdf"
        }
    )
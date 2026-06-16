from fastapi import APIRouter, UploadFile, File, Form
from src.services.resume_service import ResumeService
from src.services.user_profile_service import UserProfileService

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.post("/generate")
async def generate_profile(
    resume: UploadFile = File(...),

    communication_score: int = Form(...),
    coding_score: int = Form(...),
    aptitude_score: int = Form(...),
    soft_skills_score: int = Form(...),

    backlogs: int = Form(...),

    college_tier: str = Form(...),
    placement_training: str = Form(...)
):
    
    resume_service = ResumeService()
    file_content = await resume.read()

    filepath = resume_service.save_resume(file_content)
    profile_result = resume_service.parse_resume(filepath)

    form_result = {
        "communication_score": communication_score,
        "coding_score": coding_score,
        "aptitude_score": aptitude_score,
        "soft_skills_score": soft_skills_score,
        "backlogs": backlogs,
        "college_tier": college_tier,
        "placement_training": placement_training
    }

    user_profile = UserProfileService()
    result = user_profile.generate_user_profile(profile_result, form_result)
    return result
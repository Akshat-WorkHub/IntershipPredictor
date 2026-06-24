from fastapi import APIRouter, UploadFile, File, Form

from src.services.resume_service import ResumeService
from src.services.job_description_service import JobDescriptionService
from src.services.user_profile_service import UserProfileService
from src.services.feature_builder_service import FeatureBuilderService
from src.services.prediction_service import PredictionService

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.post("/generate")
async def generate_profile(
    resume: UploadFile = File(...),
    job_description: UploadFile = File(...),

    github_url: str = Form(""),
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
    profile_result = resume_service.parse(file_content)

    jd_service = JobDescriptionService()
    jd_file_content = await job_description.read()
    jd_result = jd_service.parse(jd_file_content)

    skill_gap_result = jd_service.compare_skills(
        resume_data=profile_result,
        jd_data=jd_result
    )

    form_result = {
        "github_url": github_url,
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

    feature_builder = FeatureBuilderService()
    feature_result = feature_builder.build(result)

    try:    
        prediction_service = PredictionService()
        prediction_result = prediction_service.predict(feature_result)

        prediction = prediction_result["prediction"]
        pred_prob = prediction_result["probability"]

        pred_result = ("Selected" if prediction == 1 else "Not Selected")

        return {
            "Result": pred_result,
            "prediction_probability": pred_prob,
            "skill_gap": skill_gap_result,
            "matched_skills":
                skill_gap_result["matched_skills"],

            "missing_skills":
                skill_gap_result["missing_skills"],

            "resume_data": profile_result,
            "jd_data": jd_result
        }
    
    except FileNotFoundError as e:
        return {
            "status": "error",
            "message": str(e)
        }

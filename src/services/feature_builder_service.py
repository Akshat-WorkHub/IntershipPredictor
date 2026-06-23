from src.services.github_score_service import GitHubScoreService

class FeatureBuilderService:
    def build(self, profile_data: dict) -> dict:
        """
        Converts parsed profile data into model-ready features
        that can be automatically derived from the resume/profile.
        """

        education = profile_data.get("education", [])
        github_service = GitHubScoreService()
        github_score = github_service.get_score(profile_data.get("github_url", ""))

        cgpa = 0.0
        if education:
            cgpa = education[0].get("academic_score", 0.0)

        return {
            "student_id": 0,

            "CGPA": cgpa,

            "skills_score": min(
                len(profile_data.get("skills", [])),
                10
            ),

            "projects_count": len(
                profile_data.get("projects", [])
            ),

            "internships_done": len(
                profile_data.get("internships", [])
            ),

            "communication_score":
                profile_data.get("communication_score", 0),

            "aptitude_score":
                profile_data.get("aptitude_score", 0),

            # Temporary mapping
            "coding_test_score":
                profile_data.get("coding_score", 0),

            # Placeholder for now
            "resume_score": 
                profile_data.get("resume_score", 5),

            "extracurricular":
                "Yes" if profile_data.get("extracurriculars", [])
                else "No",

            "college_tier":
                profile_data.get("college_tier", "Tier 3"),

            "hackathons_participated":
                len(profile_data.get("hackathons", [])),

            "certifications_count":
                len(profile_data.get("certifications", [])),

            # Placeholder values
            "linkedin_activity_score": 5,
            "github_score": github_score,

            "soft_skills_score":
                profile_data.get("soft_skills_score", 0),

            "interview_score": 5,
            "consistency_score":
                profile_data.get("consistency_score", 5),

            "backlogs":
                profile_data.get("backlogs", 0),

            "placement_training":
                profile_data.get("placement_training", "No")
        }
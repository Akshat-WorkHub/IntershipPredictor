from src.parsers.llm import BaseLLMService
from src.parsers.pydantic_models import JobDescriptionData
from src.parsers.loader import JobDescriptionLoader
from src.parsers.llm_prompt import jd_prompt
import os, json

class JobDescriptionService(BaseLLMService):

    schema = JobDescriptionData
    prompt_template = jd_prompt

    def __init__(self):
        super().__init__()
        
        self.project_root = os.path.abspath(os.path.join( os.path.dirname(__file__), "..", ".." ))
        self.dirpath = os.path.join(self.project_root,"new_data","job_desc")
        self.compare_skills_dir = os.path.join(self.project_root,"new_data","compare_skills")

    def parse(self, uploaded_file):
        os.makedirs(self.dirpath, exist_ok=True)
        existing_files = os.listdir(self.dirpath)
        jd_count = len(existing_files) + 1

        filepath = os.path.join(self.dirpath, f"job_desc{jd_count}.pdf")

        with open(filepath, "wb") as f:
            f.write(uploaded_file)

        jd_object = JobDescriptionLoader()
        jd_text = jd_object.get_job_description_text(filepath)

        return self.invoke_chain({
            "job_description_text": jd_text
        })

    def compare_skills(self, resume_data: dict, jd_data: dict):
        resume_skills = set( skill.lower() for skill in resume_data.get("skills", []) )
        jd_skills = set( skill.lower() for skill in jd_data.get("required_skills",[]) )

        matched_skills = list(
            resume_skills.intersection(jd_skills)
        )

        missing_skills = list(
            jd_skills - resume_skills
        )

        match_percentage = 0

        if len(jd_skills) > 0:
            match_percentage = round((len(matched_skills) / len(jd_skills)) * 100, 2)

        result = {
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "match_percentage": match_percentage
        }
        
        os.makedirs(self.compare_skills_dir, exist_ok=True)
        existing_files = os.listdir(self.compare_skills_dir)
        count = len(existing_files) + 1
        
        filepath = os.path.join(self.compare_skills_dir, f"compare{count}.json")

        with open(filepath,"w") as file:
            json.dump(result, file, indent=4)

        return result 
    
    
from src.parsers.llm_parser import LLMJDParser
import os, json

class JobDescriptionService:
    def __init__(self):
        self.project_root = os.path.abspath(os.path.join( os.path.dirname(__file__), "..", ".." ))
        self.dirpath = os.path.join(self.project_root,"new_data","job_desc")

    def parse_jd(self, filepath):
        llm_parser = LLMJDParser()
        return llm_parser.parse(filepath)
    
    def save_jd(self, uploaded_file):
        os.makedirs(self.dirpath, exist_ok=True)

        existing_files = os.listdir(self.dirpath)
        jd_count = len(existing_files) + 1

        filepath = os.path.join(self.dirpath, f"job_desc{jd_count}.pdf")

        with open(filepath, "wb") as f:
            f.write(uploaded_file)

        return filepath
    
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

            match_percentage = round(
                (
                    len(matched_skills)
                    / len(jd_skills)
                ) * 100,
                2
            )

        result = {
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "match_percentage": match_percentage
        }

        directory = os.path.join(self.project_root,"new_data","compare_skills")
        os.makedirs(directory, exist_ok=True)

        existing_files = os.listdir(directory)
        count = len(existing_files) + 1

        filepath = os.path.join(directory, f"compare{count}.json")
        with open(filepath,"w") as file:
            json.dump(result, file, indent=4)

        return result 
    
    
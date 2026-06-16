from src.parsers.llm_parser import LLMResumeParser
import os

class ResumeService:
    def __init__(self):
        project_root = os.path.abspath(os.path.join( os.path.dirname(__file__), "..", ".." ))
        self.dirpath = os.path.join(project_root,"new_data","resumes")
        
    def parse_resume(self, filepath):
        llm_parser = LLMResumeParser()
        return llm_parser.parse(filepath)
    
    def save_resume(self, uploaded_file):
        os.makedirs(self.dirpath, exist_ok=True)

        existing_files = os.listdir(self.dirpath)
        resume_count = len(existing_files) + 1

        filepath = os.path.join(self.dirpath, f"resume{resume_count}.pdf")

        with open(filepath, "wb") as f:
            f.write(uploaded_file)

        return filepath
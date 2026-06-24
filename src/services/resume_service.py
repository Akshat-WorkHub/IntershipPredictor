from src.parsers.llm import BaseLLMService
from src.parsers.pydantic_models import ResumeData
from src.parsers.llm_prompt import prompt 
from src.parsers.loader import ResumeLoader
import os

class ResumeService(BaseLLMService):

    schema = ResumeData
    prompt_template = prompt

    def __init__(self):
        super().__init__()
        project_root = os.path.abspath(os.path.join( os.path.dirname(__file__), "..", ".." ))
        self.dirpath = os.path.join(project_root,"new_data","resumes")


    def parse(self, uploaded_file):
        os.makedirs(self.dirpath,exist_ok=True)
        existing_files = os.listdir(self.dirpath) 
        resume_count = len(existing_files)

        filepath = os.path.join(self.dirpath,f"resumer{resume_count}.pdf")

        with open(filepath, "wb") as f:
            f.write(uploaded_file)

        resume_object = ResumeLoader()
        resume_text = resume_object.generate(filepath)

        return self.invoke_chain({
            "resume_text": resume_text
        })
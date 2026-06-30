from src.parsers.llm import BaseLLMService
from src.parsers.pydantic_models import ResumeData
from src.parsers.llm_prompt import prompt 
from src.parsers.loader import ResumeLoader
import os
import tempfile

class ResumeService(BaseLLMService):

    schema = ResumeData
    prompt_template = prompt

    def __init__(self):
        super().__init__()

    def parse(self, uploaded_file):
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        )
        filepath = temp_file.name

        try:
            with temp_file as f:
                f.write(uploaded_file)

            resume_object = ResumeLoader()
            resume_text = resume_object.generate(filepath)

        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

        return self.invoke_chain({
            "resume_text": resume_text
        })

from langchain_community.document_loaders import PyPDFLoader
from src.parsers.llm import VisionDocumentLoaderService

class BasePDFLoader:

    def extract_text(self, filepath):

        loader = PyPDFLoader(filepath)

        docs = loader.load()

        extracted_text = "\n".join(doc.page_content for doc in docs )

        if len(extracted_text.split()) >= 50:
            return extracted_text
        print("Scanned PDF detected. Switching to Vision Loader...")

        return VisionDocumentLoaderService().extract_text(filepath)


class ResumeLoader(BasePDFLoader):

    def generate(self, filepath) -> str:
        return self.extract_text(filepath)
    
class JobDescriptionLoader(BasePDFLoader):
    
    def get_job_description_text(self, filepath) -> str:
        return self.extract_text(filepath)
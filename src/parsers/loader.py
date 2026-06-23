from langchain_community.document_loaders import PyPDFLoader


class ResumeLoader:
    def generate(self, filepath) -> str:
        loader = PyPDFLoader(filepath)

        documents = loader.load()
        return "\n".join(doc.page_content for doc in documents)
    
class JobDescriptionLoader:
    def get_job_description_text(self, filepath: str) -> str:
        loader = PyPDFLoader(filepath)
        docs = loader.load()

        return "\n".join(doc.page_content for doc in docs)
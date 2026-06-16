from langchain_community.document_loaders import PyPDFLoader

class ResumeLoader:
    def generate(self, filepath):
        loader = PyPDFLoader(filepath)

        documents = loader.load()
        return "\n".join(doc.page_content for doc in documents)
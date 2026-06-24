from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

class BaseLLMService:

    schema = None
    prompt_template = None

    def __init__(self):

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0
        )

        self.structured_llm = (
            self.llm.with_structured_output(
                self.schema
            )
        )

        self.chain = self.prompt_template | self.structured_llm 

    def invoke_chain(self, payload):

        response = self.chain.invoke(payload)
        return response.model_dump()

    




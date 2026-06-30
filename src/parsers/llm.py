from pdf2image import convert_from_path
from src.parsers.llm_prompt import vision_prompt
import base64, io
import asyncio

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
load_dotenv()

class BaseLLMService:

    schema = None
    prompt_template = None
    model = "llama-3.1-8b-instant"

    def __init__(self):

        self.llm = ChatGroq(
            # model="llama-3.3-70b-versatile",
            model=self.model,
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

class VisionDocumentLoaderService:

    def __init__(self):

        self.llm = ChatGroq(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0
        )
        self.poppler_path = r'C:\Program Files\poppler-26.02.0\Library\bin'

    def encode_image(self, image):
            buffer = io.BytesIO()
            image.save(buffer,format="PNG")

            image_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
            return image_b64

    def extract_text(self, filepath: str ) -> str:
        images = convert_from_path(
            filepath,
            poppler_path=self.poppler_path
        )
        prompt = vision_prompt.format()

        extracted_text = ""

        for image in images:

            img_b64 = self.encode_image(image)
            message = HumanMessage(
                        content=[
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url":
                                    f"data:image/png;base64,{img_b64}"
                                }
                            }
                        ]
                    )

            response = self.llm.invoke([message])
            extracted_text += response.content + "\n\n"

        return extracted_text.strip()




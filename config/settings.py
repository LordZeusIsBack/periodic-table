import os
from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv("GOOGLE_API_KEY")
        self.GENERATION_CONFIGURATION = {
            "temperature": 0.1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

import os
from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()
    API_KEY = os.getenv('GEMINI_API_KEY')
    GENERATION_CONFIGURATION = {
        "temperature": 0.5,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

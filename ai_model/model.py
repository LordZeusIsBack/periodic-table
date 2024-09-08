import google.generativeai as genai
from config.settings import Config

c = Config()


class AIModel:
    def __init__(self):
        genai.configure(api_key=c.API_KEY)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=c.GENERATION_CONFIGURATION,
        )

    def start_chat_session(self):
        return self.model.start_chat(history=[])

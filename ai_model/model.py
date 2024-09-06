import google.generativeai as genai
from config.settings import Config


class AIModel:
    def __init__(self):
        genai.configure(api_key=Config.API_KEY)
        self._model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=Config.GENERATION_CONFIGURATION
        )

    def start_chat_session(self):
        return self._model.start_chat(history=[])


import google.generativeai as genai
import markdown
import html
from bs4 import BeautifulSoup


class GeminiConfig:
    _api_key = None
    _model = None
    _model_name = "gemini-2.0-flash"

    @classmethod
    def set_api_key(cls, api_key: str):
        if not api_key or not isinstance(api_key, str):
            raise ValueError("Valid API key must be a non-empty string.")
        if api_key == cls._api_key and cls._model is not None:
            print("[GeminiConfig] API key already set. Model already configured.")
            return
        cls._api_key = api_key
        try:
            genai.configure(api_key=api_key)
            cls._model = genai.GenerativeModel(cls._model_name)
            print(f"[GeminiConfig] Model '{cls._model_name}' configured successfully.")
        except Exception as e:
            cls._model = None
            raise RuntimeError(f"Failed to configure Gemini model: {e}")

    @classmethod
    def get_model(cls):
        if not cls._model:
            raise ValueError("Model not configured. Call set_api_key() first.")
        return cls._model


class GeminiResponder:
    ALLOWED_TAGS = {'p', 'table', 'tr', 'th', 'td', 'pre', 'code'}

    def __init__(self, use_markdown: bool = True):
        self.use_markdown = use_markdown

    def generate_response(self, prompt: str) -> dict:
        if not prompt or not isinstance(prompt, str):
            return {"status": False, "message": "Prompt must be a non-empty string."}
        try:
            model = GeminiConfig.get_model()
            response = model.generate_content(prompt)
            raw_text = getattr(response, "text", "")
            if not raw_text:
                return {"status": False, "message": "Model returned empty response."}

            if self.use_markdown:
                html_output = markdown.markdown(raw_text, extensions=["tables", "fenced_code"])
            else:
                safe_code = html.escape(raw_text)
                html_output = f"<pre><code>{safe_code}</code></pre>"

            soup = BeautifulSoup(html_output, 'html.parser')
            for tag in soup.find_all():
                if tag.name not in self.ALLOWED_TAGS:
                    tag.unwrap()

            return {"status": True, "response": str(soup)}

        except Exception as e:
            return {"status": False, "message": "Failed to generate content.", "error": str(e)}

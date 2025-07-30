from google import generativeai as _genai

class genai:
    """
    Top-level wrapper module to mimic:
    >>> from google import genai
    >>> client = genai.Client(api_key=...)
    """

    class Client:
        def __init__(self, api_key: str, default_model: str = "gemini-2.5-flash"):
            _genai.configure(api_key=api_key)
            self._defaultModel = default_model
            self._defaultModelInstance = _genai.GenerativeModel(model_name=default_model)

            class Models:
                def __init__(self, outer):
                    self._outer = outer

                def generate_content(self, contents: str | list[str], model: str = None, **kwargs):
                    model_name = model or self._outer._defaultModel
                    model_instance = _genai.GenerativeModel(model_name=model_name)
                    return model_instance.generate_content(contents=contents, **kwargs)

            self.models = Models(self)

        def generate(self, prompt: str | list[str], **kwargs):
            """Convenience shortcut for single-line generation."""
            return self._defaultModelInstance.generate_content(prompt, **kwargs)

        def setDefaultModel(self, model_name: str):
            """Change the default model at runtime."""
            self._defaultModel = model_name
            self._defaultModelInstance = _genai.GenerativeModel(model_name=model_name)

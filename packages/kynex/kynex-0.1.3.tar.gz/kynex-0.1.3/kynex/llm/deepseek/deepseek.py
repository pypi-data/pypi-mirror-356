from kynex.llm.base import LLMBase

class DeepSeekLLM(LLMBase):
    def __init__(self):
        # Placeholder – add real model setup later
        pass

    def get_data(self, prompt: str) -> str:
        try:
            return f"[DeepSeek Simulated Response] for: {prompt}"
        except Exception as e:
            return f"[DeepSeek ERROR]: {str(e)}"

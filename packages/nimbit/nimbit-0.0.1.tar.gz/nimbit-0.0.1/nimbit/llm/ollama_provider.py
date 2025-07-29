import ollama
from nimbit.llm.base_model_provider import BaseModelProvider
from typing import List, Dict, Any, Optional, Union

DEFAULT_OLLAMA_HOST = "http://localhost:11434"

class OllamaProvider(BaseModelProvider):
    def __init__(self, host: str = DEFAULT_OLLAMA_HOST):
        self.host = host
        self.client = ollama.Client(host=host)

    def list_models(self) -> List[Dict[str, Any]]:
        try:
            return self.client.list().get("models", [])
        except Exception as e:
            raise RuntimeError(f"Failed to list models: {e}")

    def generate(self, prompt: str, model: str = "qwen3:0.6b", options: Optional[Dict[str, Any]] = None, stream: bool = False) -> Union[str, Any]:
        try:
            if stream:
                return self.client.generate(model=model, prompt=prompt, options=options or {}, stream=True)
            else:
                result = self.client.generate(model=model, prompt=prompt, options=options or {})
                return result.get("response", "")
        except Exception as e:
            raise RuntimeError(f"Failed to generate completion: {e}")

    def embed(self, text: Union[str, List[str]], model: str = "qwen3:0.6b", options: Optional[Dict[str, Any]] = None) -> Any:
        try:
            result = self.client.embed(model=model, input=text, options=options or {})
            return result.get("embeddings", [])
        except Exception as e:
            raise RuntimeError(f"Failed to get embedding: {e}")

# For convenient import
__all__ = ["OllamaProvider", "ModelProvider"]

from typing import List, Dict, Any, Union, Optional

class BaseModelProvider:
    def list_models(self) -> List[Dict[str, Any]]:
        raise NotImplementedError

    def generate(self, prompt: str, model: str, options: Optional[Dict[str, Any]] = None, stream: bool = False) -> Union[str, Any]:
        raise NotImplementedError

    def embed(self, text: Union[str, List[str]], model: str, options: Optional[Dict[str, Any]] = None) -> Any:
        raise NotImplementedError
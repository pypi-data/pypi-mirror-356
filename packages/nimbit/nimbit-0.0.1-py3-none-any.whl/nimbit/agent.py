from typing import Callable, Any
from nimbit.mesh.message import Message
from nimbit.mesh.default_agent_runtime import default_agent_runtime

class Agent:
    def __init__(self):
        self._message_handler = None

    def on_message(self):
        def decorator(func: Callable[[Message], Any]):
            self._message_handler = func
            return func
        return decorator

    def run(self):
        if self._message_handler is None:
            raise Exception(f"No message handler registered.")
        default_agent_runtime(self._message_handler)

from typing import Literal, List, Any
from pydantic import BaseModel

class Argument(BaseModel):
    """"""
    description: str
    name: str
    type: Literal["float", "int", "bool", "str"]

class Schema(BaseModel):
    """Schemas define the items in a Message"""
    
    name: str
    description: str
    arguments: List[Argument]

    def validate(self, msg: Any):
        """Validates that a message matches the intended schema"""
        if not isinstance(msg, dict):
            raise ValueError("Message must be a dictionary.")
        
        # Check all required arguments are present and of correct type
        for arg in self.arguments:
            if arg.name not in msg:
                raise ValueError(f"Missing required argument: {arg.name}")
            value = msg[arg.name]
            expected_type = arg.type
            if expected_type == "int" and not isinstance(value, int):
                raise ValueError(f"Argument '{arg.name}' must be int, got {type(value).__name__}")
            elif expected_type == "float" and not isinstance(value, float):
                raise ValueError(f"Argument '{arg.name}' must be float, got {type(value).__name__}")
            elif expected_type == "bool" and not isinstance(value, bool):
                raise ValueError(f"Argument '{arg.name}' must be bool, got {type(value).__name__}")
            elif expected_type == "str" and not isinstance(value, str):
                raise ValueError(f"Argument '{arg.name}' must be str, got {type(value).__name__}")
        # Optionally, check for extra arguments not in schema
        schema_arg_names = {arg.name for arg in self.arguments}
        for key in msg:
            if key not in schema_arg_names:
                raise ValueError(f"Unexpected argument: {key}")
        return True

    def describe(self, examples: List[str] = []) -> str:
        """
        Generate a prompt instructing an LLM how to structure a json according to this schema.
        Optionally include example outputs.
        """
        lines = [
            f"You must output a JSON object with the following structure:",
            "Fields:",
        ]
        for arg in self.arguments:
            lines.append(f"  - {arg.name} ({arg.type}): {arg.description}")
        lines.append("\nYour output must be valid JSON and match the above structure exactly.")
        if examples:
            lines.append("\nHere are example outputs:")
            for ex in examples:
                import json
                lines.append(json.dumps(ex, indent=2))
        return "\n".join(lines)

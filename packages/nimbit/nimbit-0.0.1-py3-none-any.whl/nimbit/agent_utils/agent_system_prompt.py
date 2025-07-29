from typing import List
from pydantic import BaseModel

class ConstraintsAndLimits(BaseModel):
    max_response_tokens: int = 300
    max_tool_calls: int = 5

class SystemPrompt(BaseModel):
    
    identity_and_purpose: str
    guidelines: List[str]
    limits: ConstraintsAndLimits

    def assemble(self, body: str) -> str:
        """
        Assemble the system prompt in the following order:
        1. identity and purpose
        2. body
        3. limits
        4. guidelines
        """
        sections = []
        # 1. Identity and Purpose
        sections.append(f"Identity and Purpose:\n{self.identity_and_purpose}\n")
        # 2. Body
        sections.append(f"Task:\n{body}\n")
        # 3. Limits
        if hasattr(self.limits, 'describe'):
            limits_str = self.limits.describe()
        else:
            limits_str = str(self.limits)
        sections.append(f"Limits:\n{limits_str}\n")
        # 4. Guidelines
        if self.guidelines:
            guidelines_str = "\n".join(f"- {g}" for g in self.guidelines)
            sections.append(f"Guidelines:\n{guidelines_str}\n")
        return "\n".join(sections)

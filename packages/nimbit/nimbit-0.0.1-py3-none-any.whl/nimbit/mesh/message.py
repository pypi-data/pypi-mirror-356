from typing import Optional, List
from pydantic import BaseModel
from nimbit.mesh.schema import Argument

class Message(BaseModel):
    requestId: int

    source: str
    destination: Optional[str] = None

    metadata: dict
    content: str

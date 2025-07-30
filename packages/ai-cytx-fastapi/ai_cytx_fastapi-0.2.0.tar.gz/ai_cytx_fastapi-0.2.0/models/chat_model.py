from typing import List, Optional
from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    planId: str
    messages: List[Message]
    sessionId: Optional[str] = ""
    fileIds: Optional[List[str]] = []
    mode: Optional[int] = 0

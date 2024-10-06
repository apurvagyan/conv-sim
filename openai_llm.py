from enum import Enum
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
openai_api_key = os.getenv('OPEN_API_KEY')
client = OpenAI(api_key=openai_api_key)

class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"
    SYSTEM = "system"
    
class OpenAIMessage(BaseModel):
    content: Optional[str] = None
    role: Role
    name: Optional[str] = None
    # function_call: Optional[FunctionCall] = None
    context: Optional[str] = None
    unlabeled_context: Optional[str] = None # unlabeled context is any string that should be put directly before the content, but is not strictly memory or other formal context
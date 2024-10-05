from fastapi import FastAPI
from pydantic import BaseModel
from ConversationManager import ConversationManager

class UserPromptRequest(BaseModel):
    content: str

app = FastAPI()

@app.get("/user-prompt")
def process_user_prompt(user_prompt_request: UserPromptRequest):
    user_prompt = user_prompt_request.content
    conversation_manager = ConversationManager(user_input=user_prompt, max_exchanges=10)
    
    return {"prompt": user_prompt_request.content}
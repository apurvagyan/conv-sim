import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from ConversationManager import ConversationManager
from fastapi.middleware.cors import CORSMiddleware


class UserPromptRequest(BaseModel):
    agent_1_desc: str
    agent_2_desc: str
    prompt: str

class UserPromptResponse(BaseModel):
    messages: list[str]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/user-prompt")
def process_user_prompt(user_prompt_request: UserPromptRequest):
    user_prompt = user_prompt_request.prompt
    conversation_manager = ConversationManager(user_input=user_prompt, agent_1_desc=user_prompt_request.agent_1_desc, agent_2_desc=user_prompt_request.agent_2_desc, max_exchanges=10)
    analysis = conversation_manager.analyze_conversation()
    print("ANALYSIS \n")
    print(analysis)
    print("Conversation analyzed, returning to FE")
    return {"messages": conversation_manager.messages, "analysis": analysis}
import asyncio
import base64
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from ConversationManager import ConversationManager
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os


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
    analysis, encoded_sentiment_graph = conversation_manager.analyze_conversation()
    decoded_image = base64.b64decode(encoded_sentiment_graph)
    with open("decoded_image.png", "wb") as f:
        f.write(decoded_image)

    print("ANALYSIS \n")
    print(analysis)
    print("Conversation analyzed, returning to FE")
    return {"messages": conversation_manager.messages, "analysis": analysis, "encodedSentimentGraph": encoded_sentiment_graph}
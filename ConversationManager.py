from ContextManager import ContextManager
from prompts import KAMALA_SAMPLE_PROMPT, TRUMP_SAMPLE_PROMPT
from pydantic import BaseModel

class ConversationMessage(BaseModel):
    content: str
    speaker: int

# Logic to pass messages to each context manager and get them to generate their response, then print the response
class ConversationManager():
    def __init__(self, user_input):
        self.user_input = user_input
        system_prompts = self.generate_personality_system_prompts()
        self.context_manager_1 = ContextManager(system_prompts[0]) # pass in the prompt here?
        self.context_manager_2 = ContextManager(system_prompts[1]) # pass in the prompt here?
        self.messages = []

    
    def generate_personality_system_prompts(self):
        # generate system prompts for each personality
        system_prompts = []
        system_prompts.append(KAMALA_SAMPLE_PROMPT)
        system_prompts.append(TRUMP_SAMPLE_PROMPT)
        return system_prompts

    


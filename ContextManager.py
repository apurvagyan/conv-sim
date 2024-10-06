import openai
from openai_llm import OpenAIMessage, Role, client


# how is each context manager used - in the past i just put this all in a main.py lmfao
# is this where i create my system prompts and etc.

# Store current messages
# Has generate(), add_message() functions
class ContextManager():
    def __init__(self, system_prompt):
        self.system_prompt = system_prompt
        self.messages = []
        self.messages.append(OpenAIMessage(content=self.system_prompt, role=Role.SYSTEM))
    
    def generate_response(self):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=self.messages,
            temperature=0.7
        )
        
        self.messages.append(OpenAIMessage(content=response.choices[0].message.content, role=Role.ASSISTANT))
        return response.choices[0].message.content
    
    def add_message(self, message):
        self.messages.append(OpenAIMessage(content=message, role=Role.USER))
    

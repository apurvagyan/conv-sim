import openai
from openai_llm import OpenAIMessage, Role

# how is each context manager used - in the past i just put this all in a main.py lmfao
# is this where i create my system prompts and etc.

# Store current messages
# Has generate(), add_message() functions
class ContextManager():
    def __init__(self, system_prompt):
        self.system_prompt = system_prompt
        self.messages = []
        self.messages.append(OpenAIMessage(content=self.system_prompt, role=Role.SYSTEM))
    
    def generate_response(self, prompt, message):
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": message}
        ]
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150
        )
        
        self.messages.append(OpenAIMessage(content=response.choices[0].message['content'], role=Role.ASSISTANT))
        return response.choices[0].message['content']
    

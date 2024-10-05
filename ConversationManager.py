from ContextManager import ContextManager
from prompts import KAMALA_SAMPLE_PROMPT, TRUMP_SAMPLE_PROMPT
from pydantic import BaseModel
from uagents import Agent, Context, Model, Bureau


# class ConversationMessage(BaseModel):
#     content: str
#     speaker: int

class Message(Model):
    content: str

# Logic to pass messages to each context manager and get them to generate their response, then print the response
class ConversationManager():
    def __init__(self, user_input, max_exchanges):
        self.user_input = user_input
        self.max_exchanges = max_exchanges
        self.exchange_count = 0
        system_prompts = self.generate_personality_system_prompts()
        self.context_manager_1 = ContextManager(system_prompts[0]) # pass in the prompt here?
        self.context_manager_2 = ContextManager(system_prompts[1]) # pass in the prompt here?
        self.agent_1 = Agent(
            name="agent_1",
            port=8000,
            seed="agent_1",
        )
        self.agent_2 = Agent(
            name="agent_2",
            port=8001,
            seed="agent_2",
        )

        @self.agent_1.on_message(model=Message)
        async def agent_1_respond(ctx: Context, sender: str, msg: Message):
            if self.exchange_count >= max_exchanges:
                print("Conversation has ended.")
                return

            # print(f"\nDonald Trump: {msg.content}")
            self.context_manager_1.add_message(msg.content)
            response = self.context_manager_1.generate_response()
            print(f"Agent 1: {response}")
            exchange_count += 1
            await ctx.send(self.agent_2.address, Message(content=response))

        @self.agent_2.on_message(model=Message)
        async def agent_2_respond(ctx: Context, sender: str, msg: Message):
            if self.exchange_count >= max_exchanges:
                print("Conversation has ended.")
                return

            # print(f"\nDonald Trump: {msg.content}")
            self.context_manager_2.add_message(msg.content)
            response = self.context_manager_2.generate_response()
            print(f"Agent 2: {response}")
            self.exchange_count += 1
            await ctx.send(self.agent_2.address, Message(content=response))

        # Function to initiate the conversation
        @self.agent_1.on_interval(period=5.0)
        async def start_conversation(ctx: Context):
            if self.exchange_count == 0:
                initial_message = "What are your thoughts on climate change and its impact on our nation?"
                print(f"\nInitial question: {initial_message}")
                self.exchange_count += 1
                await ctx.send(self.agent_2.address, Message(content=initial_message))
        self.messages = []

        self.bureau = Bureau(port=8080, endpoint="http://127.0.0.1:8080/submit")
        self.bureau.add(self.agent_1)
        self.bureau.add(self.agent_2)
        self.bureau.run()

    
    def generate_personality_system_prompts(self):
        # generate system prompts for each personality
        system_prompts = []
        system_prompts.append(KAMALA_SAMPLE_PROMPT)
        system_prompts.append(TRUMP_SAMPLE_PROMPT)
        return system_prompts

    


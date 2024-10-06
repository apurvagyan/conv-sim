import asyncio
import time
from ContextManager import ContextManager
from chitchat import ChitChatDialogue
from prompts import KAMALA_SAMPLE_PROMPT, TRUMP_SAMPLE_PROMPT, SYSTEM_PROMPT_GEN_PROMPT
from pydantic import BaseModel
from uagents import Agent, Context, Model, Bureau
from openai_llm import OpenAI, client
from uagents.query import query
# from ConversationManager import ConversationManager, ConversationMessage
from structs import MessageWithManager

agent_1 = Agent(
    name="agent_1",
    port=8000,
    seed="agent_1_1111",
    endpoint="http://127.0.0.1:8000/submit",

)

@agent_1.on_message(model=MessageWithManager)
async def agent_1_respond(ctx: Context, sender: str, msg: MessageWithManager):
    manager = msg.conversation_manager
    if manager.exchange_count >= manager.max_exchanges:
        print("Conversation has ended.")
        # await ctx.send(self.agent_1.address, ConcludeChitChatDialogue())
        return

    # print(f"\nDonald Trump: {msg.content}")
    manager.context_manager_1.add_message(msg.content)
    response = manager.context_manager_1.generate_response()
    print(f"{manager.agent_1.name}: {response}")
    manager.messages.append(ConversationMessage(content=response, speaker=1))
    manager.exchange_count += 1
    await ctx.send(manager.agent_2.address, MessageWithManager(content=response, conversation_manager=manager))

print(agent_1.address)

if __name__=="__main__":
    agent_1.run()
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

agent_2 = Agent(
    name="agent_2",
    port=8001,
    seed="agent_2_2222",
    endpoint="http://127.0.0.1:8001/submit",

)

@agent_2.on_query(model=MessageWithManager)
async def query_handler(ctx: Context, sender: str, msg: MessageWithManager):
    print("Query received")
    manager = msg.conversation_manager
    if manager.exchange_count >= manager.max_exchanges:
        print("Conversation has ended.")
        # await ctx.send(self.agent_1.address, ConcludeChitChatDialogue())
        return

    # print(f"\nDonald Trump: {msg.content}")
    manager.context_manager_2.add_message(msg.content)
    response = manager.context_manager_2.generate_response()
    print(f"{manager.agent_2.name}: {response}")
    manager.messages.append(ConversationMessage(content=response, speaker=2))
    manager.exchange_count += 1
    await ctx.send(manager.agent_1.address, MessageWithManager(content=response, conversation_manager=manager))
    # pass

@agent_2.on_message(model=MessageWithManager)
async def agent_2_respond(ctx: Context, sender: str, msg: MessageWithManager):
    manager = msg.conversation_manager
    if manager.exchange_count >= manager.max_exchanges:
        print("Conversation has ended.")
        # await ctx.send(self.agent_1.address, ConcludeChitChatDialogue())
        return

    # print(f"\nDonald Trump: {msg.content}")
    manager.context_manager_2.add_message(msg.content)
    response = manager.context_manager_2.generate_response()
    print(f"{manager.agent_2.name}: {response}")
    manager.messages.append(ConversationMessage(content=response, speaker=2))
    manager.exchange_count += 1
    await ctx.send(manager.agent_1.address, MessageWithManager(content=response, conversation_manager=manager))

if __name__=="__main__":
    agent_2.run()
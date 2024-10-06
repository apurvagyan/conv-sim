import asyncio
import openai
from openai_llm import OpenAIMessage, Role
from ConversationManager import ConversationManager

# Set up a manager for both identities in the conversation
# Set up a context manager for each person in the conversation, 
# has pass_message function to pass message to the other context 
if __name__ == "__main__":
    agent_1_desc = "Kamala"
    agent_2_desc = "Trump"
    conversation_manager = ConversationManager(user_input="Simulate Kamala and Trump talking about climate change", agent_1_desc=agent_1_desc, agent_2_desc=agent_2_desc, max_exchanges=5)
    # conversation_messages = asyncio.run(conversation_manager.start_conversation())
    print(conversation_manager.messages)

    analysis = conversation_manager.analyze_conversation()
    print(analysis)





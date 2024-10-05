import openai
from openai_llm import OpenAIMessage, Role
from ConversationManager import ConversationManager

# Set up a manager for both identities in the conversation
# Set up a context manager for each person in the conversation, 
# has pass_message function to pass message to the other context 
if __name__ == "__main__":
    conversation_manager = ConversationManager(user_input="Simulate Kamala and Trump talking about climate change", max_exchanges=10)





from uagents import Model
from ConversationManager import ConversationManager

class MessageWithManager(Model):
    content: str
    conversation_manager: ConversationManager
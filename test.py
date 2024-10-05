from uagents import Agent, Context, Model, Bureau
from openai import OpenAI
import os
from dotenv import load_dotenv
import socket
import time
import threading
import asyncio

# Load the .env file
load_dotenv()

# Set OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)

class Message(Model):
    content: str

BASE_PROMPT = """Generate an identity which is rigorously accurate. It should mimic:
1) The language and tone with which that person speaks
2) The beliefs and values they hold
3) The way they would generally behaviorally operate
4) The real details known regarding their identity, including location, upbringing, culture, and style of conversation

Based on this, create a character with the following details. NOTE, please respond as if you ARE the character
that you have just created. You should embody their language, tone, beliefs, values, background and information set.
If they are known to be mean, don't be afraid to be mean. If they are kind, don't be afraid to be kind. Replicate
EXACTLY how they would actually care to respond in the real world setting. DO NOT allow the conversation to be 
influenced by the bounds of AI-chat conversation. They should talk like the real people that they are and represent.
These instructions should be included in the system prompt description which you create for the identity."""

# Global variables
max_exchanges = 6
exchange_count = 0
agent1_prompt = ""
agent2_prompt = ""
conversation_topic = ""
conversation_log = []

# Global event to signal conversation end
conversation_ended = threading.Event()

def generate_personality_system_prompts(character1, character2):
    prompt1 = f"{BASE_PROMPT} {character1}"
    prompt2 = f"{BASE_PROMPT} {character2}"
    
    identity1 = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt1}],
        max_tokens=300
    ).choices[0].message.content

    identity2 = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt2}],
        max_tokens=300
    ).choices[0].message.content

    return identity1, identity2

def generate_response(prompt, message):
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": message}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=150
    )
    
    return response.choices[0].message.content

def find_free_port(start_port=8080, max_port=9000):
    for port in range(start_port, max_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('', port))
                return port
            except OSError:
                continue
    raise IOError("No free ports")

# Create agents
agent1 = Agent(
    name="agent1",
    port=find_free_port(8000),
    seed="agent1_secret_phrase",
)

agent2 = Agent(
    name="agent2",
    port=find_free_port(8001),
    seed="agent2_secret_phrase",
)

# Agent1 behavior
@agent1.on_message(model=Message)
async def agent1_respond(ctx: Context, sender: str, msg: Message):
    global exchange_count, conversation_log
    if exchange_count >= max_exchanges:
        print("Conversation has ended.")
        conversation_ended.set()  # Set the event
        return

    response = generate_response(agent1_prompt, f"{msg.content}\nRespond: {conversation_topic}")
    print(f"Agent 1: {response}")
    conversation_log.append(f"Agent 1: {response}")
    exchange_count += 1
    await ctx.send(agent2.address, Message(content=response))

# Agent2 behavior
@agent2.on_message(model=Message)
async def agent2_respond(ctx: Context, sender: str, msg: Message):
    global exchange_count, conversation_log
    if exchange_count >= max_exchanges:
        print("Conversation has ended.")
        conversation_ended.set()  # Set the event
        return

    response = generate_response(agent2_prompt, f"{msg.content}\nRespond: {conversation_topic}")
    print(f"Agent 2: {response}")
    conversation_log.append(f"Agent 2: {response}")
    exchange_count += 1
    await ctx.send(agent1.address, Message(content=response))

# Function to initiate the conversation
@agent1.on_interval(period=5.0)
async def start_conversation(ctx: Context):
    global exchange_count, conversation_log
    if exchange_count == 0:
        initial_message = f"What are your thoughts on {conversation_topic}?"
        print(f"\nInitial question: {initial_message}")
        conversation_log.append(f"Initial question: {initial_message}")
        exchange_count += 1
        await ctx.send(agent2.address, Message(content=initial_message))

# Function to analyze the conversation
def analyze_conversation():
    conversation_text = "\n".join(conversation_log)
    analysis_prompt = f"""Analyze the following conversation and provide:
    1. Key takeaways
    2. Major points discussed
    3. General productivity assessment
    4. Any interesting insights or observations

    Please be succinct but clear, providing a high-impact analysis.

    Conversation:
    {conversation_text}
    """

    analysis = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an expert conversation analyst."},
                  {"role": "user", "content": analysis_prompt}],
        max_tokens=300
    ).choices[0].message.content

    return analysis

# Function to run the bureau
def run_bureau(bureau):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bureau.run())

# Function to monitor conversation and stop bureau
def monitor_conversation(bureau_thread):
    conversation_ended.wait()  # Wait for the conversation to end
    print("\nStopping the bureau...")
    # Forcefully stop the bureau thread
    bureau_thread.join(timeout=1)
    if bureau_thread.is_alive():
        # If thread is still alive, we need to forcefully terminate it
        # This is not ideal, but necessary given the constraints
        import _thread
        _thread.interrupt_main()

if __name__ == "__main__":
    # Ask user for character descriptions
    character1 = input("Enter a brief description for the first character (e.g., 'A 45-year-old environmental scientist from California'): ")
    character2 = input("Enter a brief description for the second character (e.g., 'A 60-year-old oil company executive from Texas'): ")
    
    # Generate personalized system prompts
    agent1_prompt, agent2_prompt = generate_personality_system_prompts(character1, character2)
    
    print("\nGenerated Character Profiles:")
    print(f"Character 1:\n{agent1_prompt}\n")
    print(f"Character 2:\n{agent2_prompt}\n")
    
    # Ask for the conversation topic
    conversation_topic = input("Enter the main topic for the conversation: ")
    
    print("\nStarting conversation...")
    
    # Create the bureau
    bureau_port = find_free_port()
    bureau = Bureau(port=bureau_port, endpoint=f"http://127.0.0.1:{bureau_port}/submit")
    bureau.add(agent1)
    bureau.add(agent2)
    
    # Start the bureau in a separate thread
    bureau_thread = threading.Thread(target=run_bureau, args=(bureau,))
    bureau_thread.start()

    # Start monitoring thread
    monitor_thread = threading.Thread(target=monitor_conversation, args=(bureau_thread,))
    monitor_thread.start()

    try:
        # Wait for the monitoring thread to finish
        monitor_thread.join()
    except KeyboardInterrupt:
        print("\nConversation interrupted by user.")
    finally:
        # After the conversation ends, analyze it
        print("\nAnalyzing the conversation...")
        analysis = analyze_conversation()
        print("\nConversation Analysis:")
        print(analysis)
        

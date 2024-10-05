from uagents import Agent, Context, Model, Bureau
import openai
from openai import OpenAI

# Set your OpenAI API key
openai_api_key = "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"
client = OpenAI(api_key=openai_api_key)

class Message(Model):
    content: str

# Define the prompts for each agent
kamala_prompt = "You are Kamala Harris, the Vice President of the United States. You believe in addressing climate change and support aggressive policies to reduce emissions and promote clean energy. Respond to the previous message about climate change."
trump_prompt = "You are Donald Trump, the former President of the United States. You are skeptical of the severity of climate change and prioritize economic growth over environmental regulations. Respond to the previous message about climate change."

def generate_response(prompt, message):
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": message}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=150
    )
    
    return response.choices[0].message.content

# Create Kamala Harris agent
kamala = Agent(
    name="kamala_harris",
    port=8000,
    seed="kamala_secret_phrase",
)

# Create Donald Trump agent
trump = Agent(
    name="donald_trump",
    port=8001,
    seed="trump_secret_phrase",
)

# Global variables to control the conversation
max_exchanges = 6
exchange_count = 0

# Kamala Harris agent behavior
@kamala.on_message(model=Message)
async def kamala_respond(ctx: Context, sender: str, msg: Message):
    global exchange_count
    if exchange_count >= max_exchanges:
        print("Conversation has ended.")
        return

    # print(f"\nDonald Trump: {msg.content}")
    response = generate_response(kamala_prompt, msg.content)
    print(f"Kamala Harris: {response}")
    exchange_count += 1
    await ctx.send(trump.address, Message(content=response))

# Donald Trump agent behavior
@trump.on_message(model=Message)
async def trump_respond(ctx: Context, sender: str, msg: Message):
    global exchange_count
    if exchange_count >= max_exchanges:
        print("Conversation has ended.")
        return

    # print(f"\nKamala Harris: {msg.content}")
    response = generate_response(trump_prompt, msg.content)
    print(f"Donald Trump: {response}")
    exchange_count += 1
    await ctx.send(kamala.address, Message(content=response))

# Function to initiate the conversation
@kamala.on_interval(period=5.0)
async def start_conversation(ctx: Context):
    global exchange_count
    if exchange_count == 0:
        initial_message = "What are your thoughts on climate change and its impact on our nation?"
        print(f"\nInitial question: {initial_message}")
        exchange_count += 1
        await ctx.send(trump.address, Message(content=initial_message))

if __name__ == "__main__":
    bureau = Bureau(port=8080, endpoint="http://127.0.0.1:8080/submit")
    bureau.add(kamala)
    bureau.add(trump)
    bureau.run()
    
import asyncio
import socket
import threading
import time
from ContextManager import ContextManager
from chitchat import ChitChatDialogue
from prompts import KAMALA_SAMPLE_PROMPT, TRUMP_SAMPLE_PROMPT, SYSTEM_PROMPT_GEN_PROMPT
from pydantic import BaseModel
from uagents import Agent, Context, Model, Bureau
from openai_llm import OpenAI, client
from uagents.query import query
# from agent1 import agent_1
# from agent2 import agent_2



class ConversationMessage(BaseModel):
    content: str
    speaker: int

class Message(Model):
    content: str

# Define dialogue messages; each transition needs a separate message
class InitiateChitChatDialogue(Model):
    pass
 
class AcceptChitChatDialogue(Model):
    pass
 
class ChitChatDialogueMessage(Model):
    text: str
 
class ConcludeChitChatDialogue(Model):
    pass
 
class RejectChitChatDialogue(Model):
    pass

# Logic to pass messages to each context manager and get them to generate their response, then print the response
class ConversationManager():
    def __init__(self, user_input, agent_1_desc, agent_2_desc, max_exchanges):
        self.user_input = user_input
        self.agent_1_desc = agent_1_desc
        self.agent_2_desc = agent_2_desc
        self.max_exchanges = max_exchanges
        self.exchange_count = 0
        self.messages = []

        # Initialize agents
        loop = asyncio.new_event_loop()
        print(f"Loop is running: {loop.is_running()}")
        print(f"Loop time: {loop.time()}")
        print(f"Total tasks: {len(asyncio.all_tasks(loop))}")
        self.agent_1 = Agent(
            name=agent_1_desc,
            port=8000,
            seed="agent_1",
            loop=loop,
        )
        # self.agent_1 = agent_1

        self.agent_2 = Agent(
            name=agent_2_desc,
            port=8001,
            seed="agent_2",
            endpoint=["http://127.0.0.1:8001/submit"],
            loop=loop,
        )
        # self.agent_2 = agent_2

        prompt_1, prompt_2 = self.generate_personality_system_prompts()
        print(f"Prompt 1: {prompt_1}")
        print(f"Prompt 2: {prompt_2}")
        self.context_manager_1 = ContextManager(prompt_1) # pass in the prompt here?
        self.context_manager_2 = ContextManager(prompt_2) # pass in the prompt here?

        @self.agent_1.on_message(model=Message)
        async def agent_1_respond(ctx: Context, sender: str, msg: Message):
            if self.exchange_count >= max_exchanges:
                print("Conversation has ended.")
                self.conversation_ended.set()  # Set the event
                # await ctx.send(self.agent_2.address, ConcludeChitChatDialogue())
                return

            # print(f"\nDonald Trump: {msg.content}")
            self.context_manager_1.add_message(msg.content)
            response = self.context_manager_1.generate_response()
            print(f"{self.agent_1.name}: {response}")
            self.messages.append(ConversationMessage(content=response, speaker=1))
            self.exchange_count += 1
            await ctx.send(self.agent_2.address, Message(content=response))

        @self.agent_2.on_message(model=Message)
        async def agent_2_respond(ctx: Context, sender: str, msg: Message):
            if self.exchange_count >= self.max_exchanges:
                print("Conversation has ended.")
                self.conversation_ended.set()  # Set the event
                # await ctx.send(self.agent_1.address, ConcludeChitChatDialogue())
                return

            # print(f"\nDonald Trump: {msg.content}")
            self.context_manager_2.add_message(msg.content)
            response = self.context_manager_2.generate_response()
            print(f"{self.agent_2.name}: {response}")
            self.messages.append(ConversationMessage(content=response, speaker=2))
            self.exchange_count += 1
            await ctx.send(self.agent_1.address, Message(content=response))

        @self.agent_2.on_query(model=Message)
        async def query_handler(ctx: Context, sender: str, msg: Message):
            ctx.logger.info(f"Received query from {sender}")

            # This will be the first message, handle same way as on_message decorator
            self.context_manager_2.add_message(msg.content)
            response = self.context_manager_2.generate_response()
            print(f"{self.agent_2.name}: {response}")
            self.messages.append(ConversationMessage(content=response, speaker=2))
            self.exchange_count += 1
            await ctx.send(self.agent_1.address, Message(content=response))

        # Function to initiate the conversation
        @self.agent_1.on_interval(period=5.0)
        async def start_conversation(ctx: Context):
            if self.exchange_count == 0:
                initial_message = self.user_input
                print(f"\nInitial question: {initial_message}")
                self.exchange_count += 1
                await ctx.send(self.agent_2.address, Message(content=initial_message))

        bureau_port = self.find_free_port()

        bureau = Bureau(port=bureau_port, endpoint=f"http://127.0.0.1:{bureau_port}/submit", loop=loop)
        bureau.add(self.agent_1)
        bureau.add(self.agent_2)

        self.conversation_ended = threading.Event()

        # Start the bureau in a separate thread
        bureau_thread = threading.Thread(target=self.run_bureau, args=(bureau,))
        bureau_thread.start()

        # Start monitoring thread
        monitor_thread = threading.Thread(target=self.monitor_conversation, args=(bureau_thread,))
        monitor_thread.start()

        try:
            # Wait for the monitoring thread to finish
            monitor_thread.join()
        except KeyboardInterrupt:
            print("\nConversation interrupted by user.")
        print("ConversationManager initialized.")

    async def initialize(self):
        pass
    # Function to run the bureau
    def run_bureau(self, bureau: Bureau):
        # try:
        #     # Try to get the current running event loop
        #     loop = asyncio.get_running_loop()
        # except RuntimeError:
        #     # If no loop is running, create a new one
        #     asyncio.run(bureau.run())  # Use asyncio.run when no loop exists
        #     return

        # # If a loop already exists, use it
        # loop.run_until_complete(bureau.run())
        bureau.run()
        # asyncio.create_task(bureau.run_async())

    # Function to monitor conversation and stop bureau
    def monitor_conversation(self, bureau_thread):
        self.conversation_ended.wait()  # Wait for the conversation to end
        print("\nStopping the bureau...")
        # Forcefully stop the bureau thread
        bureau_thread.join(timeout=1)
        if bureau_thread.is_alive():
            # If thread is still alive, we need to forcefully terminate it
            # This is not ideal, but necessary given the constraints
            print("Killing bureau thread")
            import _thread
            _thread.interrupt_main()

    def find_free_port(self, start_port=8080, max_port=9000):
        for port in range(start_port, max_port):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(('', port))
                    return port
                except OSError:
                    continue
        raise IOError("No free ports")
    
    def analyze_conversation(self):
        conversation_text = "\n".join([message.content for message in self.messages])
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
    
    def agent_1_respond(self):
        if self.exchange_count >= self.max_exchanges:
            print("Conversation has ended.")
            # await ctx.send(self.agent_2.address, ConcludeChitChatDialogue())
            return

        # print(f"\nDonald Trump: {msg.content}")
        if self.messages:
            self.context_manager_1.add_message(self.messages[-1].content)
        response = self.context_manager_1.generate_response()
        print(f"{self.agent_1.name}: {response}")
        self.messages.append(ConversationMessage(content=response, speaker=1))
        self.exchange_count += 1

    def agent_2_respond(self):
        if self.exchange_count >= self.max_exchanges:
            print("Conversation has ended.")
            # await ctx.send(self.agent_2.address, ConcludeChitChatDialogue())
            return

        # print(f"\nDonald Trump: {msg.content}")
        if self.messages:
            self.context_manager_2.add_message(self.messages[-1].content)
        response = self.context_manager_2.generate_response()
        print(f"{self.agent_2.name}: {response}")
        self.messages.append(ConversationMessage(content=response, speaker=2))
        self.exchange_count += 1

    async def start_conversation(self):
        # While exchange_count < max_exchanges, keep getting responses from agent 1 or 2, alternate
        # last_spoke = 2
        # while self.exchange_count < self.max_exchanges:
        #     if last_spoke == 2:
        #         self.agent_1_respond()
        #         last_spoke = 1
        #     else:
        #         self.agent_2_respond()
        #         last_spoke = 2

        # Run the event loop to keep the bureau running
        # return asyncio.run(self.run_until_max_exchanges())
        # _ = await query(destination=self.agent_2.address, message=Message(content="start conversation"), timeout=15)
        # print("Query sent.")
        # while self.exchange_count < self.max_exchanges:
        #     await asyncio.sleep(1)
        
        return self.messages
    
    def generate_personality_system_prompts(self):
        # generate system prompts for each personality
        # system_prompts = []
        # system_prompts.append(KAMALA_SAMPLE_PROMPT)
        # system_prompts.append(TRUMP_SAMPLE_PROMPT)
        prompt1 = f"{SYSTEM_PROMPT_GEN_PROMPT} {self.agent_1_desc}"
        prompt2 = f"{SYSTEM_PROMPT_GEN_PROMPT} {self.agent_2_desc}"
        
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
    
    def initialize_chitchat_handlers(self):
        @self.chitchat_dialogue_1.on_initiate_session(InitiateChitChatDialogue)
        async def start_chitchat(
            ctx: Context,
            sender: str,
            _msg: InitiateChitChatDialogue,
        ):
            ctx.logger.info(f"Received init message from {sender}")
            # Do something when the dialogue is initiated
            await ctx.send(sender, AcceptChitChatDialogue())
        
        @self.chitchat_dialogue_1.on_start_dialogue(AcceptChitChatDialogue)
        async def accept_chitchat(
            ctx: Context,
            sender: str,
            _msg: AcceptChitChatDialogue,
        ):
            ctx.logger.info(
                f"session with {sender} was accepted. I'll say 'Hello!' to start the ChitChat"
            )
            # Do something after the dialogue is started; e.g. send a message
            await ctx.send(sender, ChitChatDialogueMessage(text="Hello!"))
        
        @self.chitchat_dialogue_1.on_reject_session(RejectChitChatDialogue)
        async def reject_chitchat(
            ctx: Context,
            sender: str,
            _msg: RejectChitChatDialogue,
        ):
            # Do something when the dialogue is rejected and nothing has been sent yet
            ctx.logger.info(f"Received reject message from: {sender}")
        
        @self.chitchat_dialogue_1.on_continue_dialogue(ChitChatDialogueMessage)
        async def continue_chitchat(
            ctx: Context,
            sender: str,
            msg: ChitChatDialogueMessage,
        ):
            # Do something when the dialogue continues
            ctx.logger.info(f"Received message: {msg.text}")
            try:
                my_msg = input("Please enter your message:\n> ")
                if my_msg != "exit":
                    await ctx.send(sender, ChitChatDialogueMessage(text=my_msg))
                else:
                    await ctx.send(sender, ConcludeChitChatDialogue())
                    ctx.logger.info(
                        f"Received conclude message from: {sender}; accessing history:"
                    )
                                # ctx.logger.info(chitchat_dialogue.get_conversation(ctx.session))
            except EOFError:
                await ctx.send(sender, ConcludeChitChatDialogue())
        
        @self.chitchat_dialogue_1.on_end_session(ConcludeChitChatDialogue)
        async def conclude_chitchat(
            ctx: Context,
            sender: str,
            _msg: ConcludeChitChatDialogue,
        ):
            # Do something when the dialogue is concluded after messages have been exchanged
            ctx.logger.info(f"Received conclude message from: {sender}; accessing history:")
            # ctx.logger.info(chitchat_dialogue.get_conversation(ctx.session))

        @self.chitchat_dialogue_2.on_initiate_session(InitiateChitChatDialogue)
        async def start_chitchat(
            ctx: Context,
            sender: str,
            _msg: InitiateChitChatDialogue,
        ):
            ctx.logger.info(f"Received init message from {sender}")
            # Do something when the dialogue is initiated
            await ctx.send(sender, AcceptChitChatDialogue())
        
        @self.chitchat_dialogue_2.on_start_dialogue(AcceptChitChatDialogue)
        async def accept_chitchat(
            ctx: Context,
            sender: str,
            _msg: AcceptChitChatDialogue,
        ):
            ctx.logger.info(
                f"session with {sender} was accepted. I'll say 'Hello!' to start the ChitChat"
            )
            # Do something after the dialogue is started; e.g. send a message
            await ctx.send(sender, ChitChatDialogueMessage(text="Hello!"))
        
        @self.chitchat_dialogue_2.on_reject_session(RejectChitChatDialogue)
        async def reject_chitchat(
            ctx: Context,
            sender: str,
            _msg: RejectChitChatDialogue,
        ):
            # Do something when the dialogue is rejected and nothing has been sent yet
            ctx.logger.info(f"Received reject message from: {sender}")
        
        @self.chitchat_dialogue_2.on_continue_dialogue(ChitChatDialogueMessage)
        async def continue_chitchat(
            ctx: Context,
            sender: str,
            msg: ChitChatDialogueMessage,
        ):
            # Do something when the dialogue continues
            ctx.logger.info(f"Received message: {msg.text}")
            try:
                my_msg = input("Please enter your message:\n> ")
                if my_msg != "exit":
                    await ctx.send(sender, ChitChatDialogueMessage(text=my_msg))
                else:
                    await ctx.send(sender, ConcludeChitChatDialogue())
                    ctx.logger.info(
                        f"Received conclude message from: {sender}; accessing history:"
                    )
                                # ctx.logger.info(chitchat_dialogue.get_conversation(ctx.session))
            except EOFError:
                await ctx.send(sender, ConcludeChitChatDialogue())
        
        @self.chitchat_dialogue_2.on_end_session(ConcludeChitChatDialogue)
        async def conclude_chitchat(
            ctx: Context,
            sender: str,
            _msg: ConcludeChitChatDialogue,
        ):
            # Do something when the dialogue is concluded after messages have been exchanged
            ctx.logger.info(f"Received conclude message from: {sender}; accessing history:")
            # ctx.logger.info(chitchat_dialogue.get_conversation(ctx.session))
    


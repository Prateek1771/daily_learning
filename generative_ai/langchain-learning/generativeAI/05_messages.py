# Messages

# Messages are the fundamental unit of context for models in Langchain, they represent the input and output of models, carrying both the content and metadata needed to represent the state of a conversation when integrating with an llm. messages are objects that contain:
    # Role - Identifies the message type (e.g.system, user)
    # Content - Represents the actual content of the message (like text, images, audio, documents, etc)
    # metadata - Optional fields such as responses information, message IDs, and token usage

# Langchain provides a standard message type that works across all model providers, ensuring consistant behavior regardless of the model being called.

import os
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

model=ChatGroq(model="qwen/qwen3-32b")

from langchain.messages import SystemMessage, HumanMessage, AIMessage

# Example 1
# messages = [
#     SystemMessage("You are a Data Science expert"),
#     HumanMessage("Explain about RAG Applications")
# ]
# res = model.invoke(messages)
# print(res.content)

# Example 2
# System_msg=SystemMessage("You are a helpful coding assistant")
# messages=[
#     System_msg,
#     HumanMessage("How do i create a REST API"),
# ]
# res = model.invoke(messages)
# print(res.content)

# Example 3
# system_msg = SystemMessage("""
#     You are a Senior Python developer with expertise in web frameworks. Always provide code examples and explain your reasoning. Be concise but through in your explanations.
# """)
# messages = [
#     system_msg,
#     HumanMessage("How do i create REST API"),
# ]
# res = model.invoke(messages)
# print(res.content)

# Example 3
# human_msg = HumanMessage(
#     content="hello!",
#     name="Prateek",
#     id="msg_123"
# )
# res = model.invoke([
#     human_msg
# ])
# print(res.content)

# Example 4
# create a AI message manually (eg., for conversation history)
# ai_msg=AIMessage("I'd be happy to help you with that question!")
# Add to conversation history
# messages=[
#     SystemMessage("You are a helpful assistant"),
#     HumanMessage("Can you help me?"),
#     ai_msg,
#     HumanMessage("Great! what's 2+1"),
# ]
# res=model.invoke(messages)
# print(res.content)
# print(res.usage_metadata)

#===============================================================================

from langchain.messages import ToolMessage
from langchain.messages import AIMessage

# after a model makes a tool call
# (here, we demonstrate manually creating the messages for brevity)
ai_message=AIMessage(
    content=[],
    tool_calls=[{
        "name":"get_weather",
        "args":{"loaction":"Bengaluru"},
        "id":"call_123"
    }]
)

# Executr tool and create result message
weather_result="Sunny, 72F"
tool_message=ToolMessage(
    content=weather_result,
    tool_call_id="call123",
)

# continue conversation
messages=[
    HumanMessage("What's the weather in the Bengaluru"),
    ai_message, # models tool call
    tool_message, # tool execution result
]
response = model.invoke(messages)
print(response.content)
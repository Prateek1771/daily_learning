import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")

from langchain.tools import tool

@tool
def get_weather(location:str)->str:
    """Get the weather at the location"""
    return f"It's sunny in {location}"

from langchain.agents import create_agent
agent=create_agent(
    model="gpt-4.1",
    tools=[get_weather],
    system_prompt="You are a helpful assistant"
)
res = agent.invoke({"messages":[{"role": "user", "content": "what is the weather in banglore"}]})
print(res)
print(res['messages'][-1].content)

# =====================================================================

from langchain_groq import ChatGroq

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

model=ChatGroq(model="qwen/qwen3-32b")

agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="you are a helpful assistant"
)
print(agent)
response=agent.invoke({"messages":[{"role":"user","content":"what is the weather like in banglore"}]})
print(response)
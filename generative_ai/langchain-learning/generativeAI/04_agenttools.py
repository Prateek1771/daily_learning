import os
from dotenv import load_dotenv
load_dotenv()

# ======================================================
# setting up llm

from langchain_groq import ChatGroq

os.environ["TAVILY_API_KEY"]=os.getenv("TAVILY_API_KEY")

model=ChatGroq(model="qwen/qwen3-32b")

# ======================================================
# search tool creation

from langchain_tavily import TavilySearch

tavily_search_tool = TavilySearch(
    max_results=5,
    topic="general",
)
# res=tavily_search_tool.invoke("what is the current news about elon musk")
# print(res)

# ============================================================

# Calculator tool
from langchain.tools import tool
@tool("calculator", description="Performs arithematic calculations. Use this for any mathematical problems.")
def calc(expression: str)-> str:
    """Evaluate mathematical expressions"""
    return str(eval(expression))

# ==================================================================

# create agents

from langchain.agents import create_agent

agent = create_agent(
    model=model,
    tools=[tavily_search_tool, calc]
)

user_input="what is the current news for anthropic and then calculate 5+5"

for step in agent.stream(
    {"messages":user_input},
    stream_mode="values"
):
    step["messages"][-1].pretty_print()

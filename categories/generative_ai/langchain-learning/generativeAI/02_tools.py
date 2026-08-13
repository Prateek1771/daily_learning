# Tools

# Models can request to call tools that perform tasks such as fetching data from a database, searching the web, or running code. Tol
# s are pairings of:
    # 1. A schema, including the name of the tool, a description, and/or arguement definitions (often a JSON schema)
    # 2. A function or coroutine to execute.
    
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

from langchain_groq import ChatGroq
model=ChatGroq(model="qwen/qwen3-32b")

from langchain.tools import tool

@tool
def get_weather(loaction:str)->str:
    """Get the weather at a location"""
    return f"It's sunny in {loaction}"

model_with_tools=model.bind_tools([get_weather])

res = model_with_tools.invoke("what is the weather in banglore")
# print(res)

# print(res.tool_calls)

#==========================================================================

# tool execution loop

# Step 1: Model genertes tool calls
message = [{"role":"user", "content":"what's the weather in Bangalore?"}]
ai_msg = model_with_tools.invoke(message)
message.append(ai_msg)

# step2: Execute tools and collect results
for tool_call in ai_msg.tool_calls:
    #execute the tool with the generated arguements
    tool_result = get_weather.invoke(tool_call)
    message.append(tool_result)
    
# step 3: Pass results back to model for final response
final_response = model_with_tools.invoke(message)
print(final_response)
import langchain
print(langchain.__version__)

import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ["GEMINI_API_KEY"]=os.getenv("GEMINI_API_KEY")
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

# =============================================================================

# Generative AI Application with OpenAI model

from langchain.chat_models import init_chat_model
model=init_chat_model("gpt-4.1")
print(model)
res = model.invoke("how does model context protocol works")
print(res)
print(res.content)

from langchain_openai import ChatOpenAI
model=ChatOpenAI(model="gpt-4.1")
res=model.invoke("hi how are u")
print(res.content)

#=====================================================================

# LLM model with gemini

from langchain.chat_models import init_chat_model
model=init_chat_model("google_genai:gemini-2.5-flash-lite")
res=model.invoke("what is ai")
print(res.content)

from langchain_google_genai import ChatGoogleGenerativeAI
model=ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
res=model.invoke("what is ai, answer in short")
print(res.content)

#=====================================================================

# LLM model with Groq

from langchain.chat_models import init_chat_model
model=init_chat_model("groq:llama-3.1-8b-instant")
res=model.invoke("tell me a joke on AI")
print(res.content)

from langchain_groq import ChatGroq
model=ChatGroq(model="qwen/qwen3-32b")
res=model.invoke("tell me a joke on ml")
print(res.content)

#=====================================================================

# streaming and batching

# Streaming - Most models can stream their output content while it is being generated. by displaying output progressively, streaming significantly imporves user experience, particularly for longer response. Calling stream() returns an iterator that yields output chunks as they are Produced. You can use a loop to process each chunk in real-time:

from langchain_groq import ChatGroq
model=ChatGroq(model="qwen/qwen3-32b")

# this waits for the total ans and then provides
res=model.invoke("tell me a joke on ml")
print(res.content)

# this displays the ans bit by bit
for chunk in model.stream("give me a 1000 words essay on AI"):
    print(chunk.text, end="|", flush=True)

for chunk in model.stream("give me a 500 words essay on my beautiful parrot"):
    print(chunk.text, end="", flush=True)
    
# Batch - Batching a collection of independent requests to a model can significantly improve performance and reduce costs, as the processing can be done in parallel:

responses= model.batch(
    [
        "why do birds fly",
        "why animals cannot fly",
        "what is the power of ai"
    ],
    config={
        "max_concurrency":5, # limit to 5 parallel calls
    }
)

for response in responses:
    print(response.content)
    
# Structured Output

# models can be requested to provide their response in a format matching a given schema.This is useful for ensuring the output can be easily parsed and used in subsequent processing.Langchain supports multiple schema types and methods for enforcing structured output.

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

os.environ["GEOQ_API_KEY"]=os.getenv("GROQ_API_KEY")

model=init_chat_model("groq:qwen/qwen3-32b")

# ================================================================================

# Pydantic
from pydantic import BaseModel, Field

# class Movie(BaseModel):
#     title:str=Field(description="the title of the movie")
#     year:str=Field(description="the year of the movie released")
#     director:str=Field(description="the director of the movie")
#     rating:str=Field(description="the rating of the movie")
#     plot:str=Field(description="the plot of the movie")
    
# model_with_structure=model.with_structured_output(Movie)

# res=model.invoke("provide details about the movie matrix")
# res2=model_with_structure.invoke("provide details about the movie matrix")

# print(res.content)
# print(res2)

# message output alongside Parsed structure

# class Movie2(BaseModel):
#     """A movie with details."""
#     title:str=Field(..., description="the title of the movie")
#     year:str=Field(..., description="the year of the movie released")
#     director:str=Field(..., description="the director of the movie")
#     rating:str=Field(..., description="the rating of the movie")
#     plot:str=Field(..., description="the plot of the movie")
    
# model_with_structure2=model.with_structured_output(Movie2)

# res3 = model_with_structure2.invoke("provide details of th movie Inception")
# print(res3)

# Nested Structure

class Actor(BaseModel):
    name:str
    role
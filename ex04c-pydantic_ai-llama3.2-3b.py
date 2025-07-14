
# Lap HP Pavilion 14
# /dev/sda3 env: nlp

# from github answers site 
# https://github.com/pydantic/pydantic-ai/issues/812
from pydantic import BaseModel
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai import Agent

#-------------------

# Example 1

class Character(BaseModel):
    name: str
    age: int

model = OpenAIModel(
    model_name = "llama3.2",
    base_url="http://localhost:11434/v1",
    api_key="ollama", # required, but unused
)

agent = Agent(model, result_type=Character)

result = agent.run_sync("Tell me about Harry Potter")
# Out[]:
TypeError: TypeAdapter.validate_json() got an unexpected keyword argument 'experimental_allow_partial'


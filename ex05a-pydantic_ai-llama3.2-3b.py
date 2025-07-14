
# Lap HP Pavilion 14
# /dev/sda3 env: nlp

# from github answers site 
# https://github.com/pydantic/pydantic-ai/issues/812
from pydantic import BaseModel
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai import Agent

#-------------------

# Example 1

model = OpenAIModel(
    model_name = "llama3.2",
    base_url="http://localhost:11434/v1",
    api_key="ollama", # required, but unused
)

agent = Agent(model)

response = agent.run_sync("What is the capital of France?")
print(response.data)
# Out[]:
# The capital of France is Paris.

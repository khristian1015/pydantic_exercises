
# PCDell7050
# /dev/sda3 env: nlp

# from Instructor site 
# https://python.useinstructor.com/examples/ollama/#patching
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List

import instructor

#-------------------

# Example 1

class Character(BaseModel):
    name: str
    age: int
    fact: List[str] = Field(..., description="A list of facts about the character")

# enables `response_model` in create call
client = instructor.from_openai(
    OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama", # required, but unused
    ),
    mode=instructor.Mode.JSON,
)

resp = client.chat.completions.create(
    model = "gemma3:12b",
    messages=[
        {
            "role": "user",
            "content": "Tell me about Harry Potter",
        }
    ],
    response_model = Character,
)
# [GIN] 2025/03/17 - 17:46:58 | 200 |          1m9s |       127.0.0.1 | POST     
# "/v1/chat/completions"
print(resp.model_dump_json(indent = 2))
# In [10]: print(resp.model_dump_json(indent = 2))
{
  "name": "Harry Potter",
  "age": 17,
  "fact": [
    "He is the central character in the Harry Potter series.",
    "He is an orphan, having lost his parents at a young age.",
    "He survived a killing curse as a baby, leaving him with a lightning bolt scar.",
    "He attends Hogwarts School of Witchcraft and Wizardry.",
    "He is known for his bravery, loyalty, and determination.",
    "He is famously 'The Boy Who Lived'.",
    "He plays Quidditch, a wizarding sport.",
    "He is often accompanied by his best friends Ron Weasley and Hermione Granger."
  ]
}

#-------------------

# https://python.useinstructor.com/

# Example 2

from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
import instructor

class ExtractUser(BaseModel):
    name: str
    age: int

client = instructor.from_openai(
    OpenAI(
        base_url = "http://localhost:11434/v1",
        api_key="ollama"
    ),
    mode=instructor.Mode.JSON,
)

resp = client.chat.completions.create(
    model = "gemma3:12b",
    messages=[
        {
            "role": "user",
            "content": "Extract Jason is 25 years old.",
        }
    ],
    response_model = ExtractUser,
)
# [GIN] 2025/03/17 - 17:53:07 | 200 | 24.741037895s |       127.0.0.1 | POST     
# "/v1/chat/completions"
print(resp.model_dump_json(indent=2))
{
  "name": "Jason",
  "age": 25
}


# LapLenovo (RAM: 8 GB)
# /dev/sda10 env: XXX

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
    model = "phi4-mini",
    messages=[
        {
            "role": "user",
            "content": "Tell me about Harry Potter",
        }
    ],
    response_model = Character,
)
# [GIN] 2025/03/16 - 19:03:34 | 200 |         1m20s |       127.0.0.1 | POST     
# "/v1/chat/completions"
# [GIN] 2025/03/16 - 19:04:08 | 200 | 22.874375781s |       127.0.0.1 | POST     "/v1/chat/completions"
# [GIN] 2025/03/16 - 19:04:28 | 200 | 19.414917604s |       127.0.0.1 | POST     "/v1/chat/completions"
# ... pydantic_core._pydantic_core.ValidationError: 1 validation error for Character age
# Input should be a valid integer [type=int_type, input_value=None, input_type=NoneType]
#     raise NotOneValueFound('Expected one value, found 0')
# executing.executing.NotOneValueFound: Expected one value, found 0
print(resp.model_dump_json(indent = 2))

# SECOND TRY
print(resp.model_dump_json(indent = 2))
# In [11]: print(resp.model_dump_json(indent = 2))
{
  "name": "Harry Potter",
  "age": 0,
  "fact": [
    "Has a lightning-shaped scar on his forehead.",
    "Born under mysterious circumstances with very rare parents' bloodline."
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
    model = "phi4-mini",
    messages=[
        {
            "role": "user",
            "content": "Extract Jason is 25 years old.",
        }
    ],
    response_model = ExtractUser,
)
#assert resp.name == "Jason"
#assert resp.age == 25

print(resp.model_dump_json(indent=2))
{
  "name": "Jason",
  "age": 25
}

#-------------------

# https://github.com/instructor-ai/instructor/blob/main/examples/patching/together.py

# Example 3

import os
import openai
from pydantic import BaseModel
import instructor

client = openai.OpenAI(
    base_url = "http://localhost:11434/v1",
    api_key="ollama"
)


# By default, the patch function will patch the ChatCompletion.create and ChatCompletion.acreate methods. to support response_model parameter
client = instructor.from_openai(client, mode=instructor.Mode.TOOLS)


# Now, we can use the response_model parameter using only a base model
# rather than having to use the OpenAISchema class
class UserExtract(BaseModel):
    name: str
    age: int


user: UserExtract = client.chat.completions.create(
    model="phi4-mini",
    response_model=UserExtract,
    messages=[
        {"role": "user", "content": "Extract jason is 25 years old"},
    ],
)  # type: ignore
#Out[]:

InstructorRetryException: Instructor does not support multiple tool calls, use List[Model] instead

print(user.model_dump_json(indent=2))
{
    "name": "Jason",
    "age": 25,
}

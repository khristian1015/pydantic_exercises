
# Lap HP Pavilion 14
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
    model = "gemma3:1b",
    messages=[
        {
            "role": "user",
            "content": "Tell me about Harry Potter",
        }
    ],
    response_model = Character,
)
# Out[]:
[GIN] 2025/03/17 - 21:55:11 | 200 |         1m57s |       127.0.0.1 | POST     "/v1/chat/completions"
[GIN] 2025/03/17 - 21:58:01 | 200 |         2m49s |       127.0.0.1 | POST     "/v1/chat/completions"
[GIN] 2025/03/17 - 22:01:39 | 200 |         3m38s |       127.0.0.1 | POST     "/v1/chat/completions"
InstructorRetryException: 1 validation error for Character
fact
  Field required [type=missing, input_value={'name': 'Harry Potter', ...rk Lord.', 'errors': []}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.9/v/missing

 ·Other kind of error in a different run
InstructorRetryException: 1 validation error for Character
fact
  Field required [type=missing, input_value={'name': 'Harry Potter', ...ice, Magic, Friendship'}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing


# SECOND TRY
[GIN] 2025/03/17 - 22:03:56 | 200 | 38.735076027s |       127.0.0.1 | POST     "/v1/chat/completions"
print(resp.model_dump_json(indent = 2))
n [8]: print(resp.model_dump_json(indent = 2))
{
  "name": "Harry Potter",
  "age": 17,
  "fact": [
    "He was born on October 31st, 1980, in Britain.",
    "He is a wizard and the son of wizard, James Potter and Lily Evans.",
    "He discovers he is a wizard when he's accidentally discovered an ancient writing on his eleventh birthday.",
    "He attends Hogwarts School of Witchcraft and Wizardry.",
    "He is fiercely loyal to his friends, Ron and Hermione, and ultimately fights against Lord Voldemort.",
    "He possesses a lightning bolt scar on his forehead, a mark of his parents' death.",
    "He has a magical owl named Hedwig.",
    "He is known for his bravery, loyalty, and sense of justice.",
    "He ultimately defeats Voldemort and restores order to the wizarding world."
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
    model = "gemma3:1b",
    messages=[
        {
            "role": "user",
            "content": "Extract Carlos is 54 years old.",
        }
    ],
    response_model = ExtractUser,
)
# [GIN] 2025/03/17 - 22:10:34 | 200 | 20.356489051s |       127.0.0.1 | POST     
# "/v1/chat/completions"

In [19]: print(resp.model_dump_json(indent=2))
{
  "name": "Carlos",
  "age": 54
}

In [20]: resp = client.chat.completions.create(
    ...:     model = "gemma3:1b",
    ...:     messages=[
    ...:         {
    ...:             "role": "user",
    ...:             "content": "We are talking about a person whose name is Car
    ...: los and I am positive that his age is 54.",
    ...:         }
    ...:     ],
    ...:     response_model = ExtractUser,
    ...: )
[GIN] 2025/03/17 - 22:12:24 | 200 |  5.427404011s |       127.0.0.1 | POST     "/v1/chat/completions"
In [21]: print(resp.model_dump_json(indent=2))
{
  "name": "Carlos",
  "age": 54
}

In [22]: resp = client.chat.completions.create(
    ...:     model = "gemma3:1b",
    ...:     messages=[
    ...:         {
    ...:             "role": "user",
    ...:             "content": "In a land far ar away, there lived an oger name
    ...: d Shrek whose age was 35.",
    ...:         }
    ...:     ],
    ...:     response_model = ExtractUser,
    ...: )
[GIN] 2025/03/17 - 22:13:37 | 200 |  5.491412351s |       127.0.0.1 | POST     "/v1/chat/completions"
In [23]: print(resp.model_dump_json(indent=2))
{
  "name": "Shrek",
  "age": 35
}

#-------------------

# https://python.useinstructor.com/

# Example 3

from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
import instructor

client = instructor.from_openai(
    OpenAI(
        base_url = "http://localhost:11434/v1",
        api_key="ollama"
    ),
    mode=instructor.Mode.JSON,
)

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

class Person(BaseModel):
    name: str
    age: int
    addresses: List[Address]

person = client.chat.completions.create(
    model="gemma3:1b",
    response_model=Person,
    messages=[
        {"role": "user", "content": """
        Extract: John Smith is 35 years old. 
        He has homes at 123 Main St, Springfield, IL 62704 and 
        456 Oak Ave, Chicago, IL 60601.
        """}
    ],
)

In [19]: print(person)
name='John Smith' age=35 addresses=[Address(street='123 Main St', city='Sprongfield', state='IL', zip_code='62704'), Address(street='456 Oak Ave', city='Chicago', state='IL', zip_code='60601')]

#Same run failed the second time (retried 2 times):
[GIN] 2025/03/22 - 11:46:14 | 200 |         3m57s |       127.0.0.1 | POST     "/v1/chat/completions"
[GIN] 2025/03/22 - 11:51:00 | 200 |         4m46s |       127.0.0.1 | POST     "/v1/chat/completions"
[GIN] 2025/03/22 - 11:56:32 | 200 |         5m31s |       127.0.0.1 | POST     "/v1/chat/completions"

InstructorRetryException: 3 validation errors for Person
name
  Field required [type=missing, input_value={'$defs': {'Address': {'s...ses', 'type': 'array'}}}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing
age
  Field required [type=missing, input_value={'$defs': {'Address': {'s...ses', 'type': 'array'}}}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing
addresses
  Field required [type=missing, input_value={'$defs': {'Address': {'s...ses', 'type': 'array'}}}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing

# THIRD TEST
[GIN] 2025/03/22 - 12:06:51 | 200 |         8m32s |       127.0.0.1 | POST     "/v1/chat/completions"

In [6]: print(person)
name='John Smith' age=35 addresses=[Address(street='123 Main St', city='Springfield', state='IL', zip_code='62704'), Address(street='456 Oak Ave', city='Chicago', state='IL', zip_code='60601')]


#-----------------------

# https://github.com/instructor-ai/instructor/blob/main/examples/patching/together.py

# Example 4

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
    model="gemma3:1b",
    response_model=UserExtract,
    messages=[
        {"role": "user", "content": "Extract jason is 25 years old"},
    ],
)  # type: ignore
#Out[]:
InstructorRetryException: Error code: 400 - {'error': {'message': 'registry.ollama.ai/library/gemma3:1b does not support tools', 'type': 'api_error', 'param': None, 'code': None}}

print(user.model_dump_json(indent=2))
{
    "name": "Jason",
    "age": 25,
}

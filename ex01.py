# from Jason Liu's talk "Pydantic is all you need"
# https://www.youtube.com/watch?v=yj-wSRJwrrc
from datetime import datetime
from typing import Tuple, List

from pydantic import BaseModel, Field, Optional


#-------------------

# Example 1

class Delivery(BaseModel):
    timestamp: datetime
    dimensions: Tuple[int, int]

m = Delivery(timestamp='2020-01-02T03:04:05Z', dimensions=['10', '20'])
print(repr(m.timestamp))
# Out[]:
# datetime.datetime(2020, 1, 2, 3, 4, 5, tzinfo=TzInfo(UTC))

print(repr(m.dimensions))
# Out[]:
# (10, 20)

#-------------------

# Example 2

from pydantic import BaseModel, ValidationError
from typing_extensions import Annotated
from pydantic import AfterValidator

def name_space(v: str) -> str:
    if " " not in v:
        raise ValueError("Name must contain space")
    return v.lower()

class UserDetail(BaseModel):
    age: int
    name: Annotated[str, AfterValidator(name_space)]

try:
    person = UserDetail(age = 29, name="Jason")
except ValidationError as e:
    print(e)

#-------------------

# Example 3


class Query(BaseModel):
    id: int
    question: str
    dependencies: List[int] = Field(
        default_factory=list,
        description="""List of subquestions that need to be answered before we can
        ask the question. Use a subquery when anything may be unkown, and we need
        to ask multiple questions to get the answer.
        Dependencies must only be other queries."""
    )

class QueryPlan(BaseModel):
    query_graph: List[Query]

query_planner(
    "What is the difference in population of Canada and Jason's home country",
)

{
    "query_graph": [
        {
            "dependencies": [],
            "id": 1,
            "question": "Identify Jason's home country"
        },
        {
            "dependencies": [],
            "id": 2,
            "question": "Find the population of Canada"
        },
        {
            "dependencies": [1],
            "id": 3,
            "question": "Find the population of jason's home country"
        },
        {
            "dependencies": [2, 3],
            "id": 4,
            "question": "Calculate the difference in populations between"
            "Canada and Json's home country",
        },
    ]
}
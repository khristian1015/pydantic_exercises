
# PC Optiplex 7050
# /dev/sda3 env: nlp2

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
    model_name = "qwen2.5:14b",
    base_url="http://localhost:11434/v1",
    api_key="ollama", # required, but unused
)

agent = Agent(
    model, 
    result_type=Character
)

result = agent.run_sync("Tell me about Harry Potter")
# Out[]: 2025MAR24
[GIN] 2025/03/24 - 03:13:47 | 200 |         2m14s |       127.0.0.1 | POST     "/v1/chat/completions"
[GIN] 2025/03/24 - 03:14:24 | 200 | 37.135825042s |       127.0.0.1 | POST     "/v1/chat/completions"

In [23]: print(result)
AgentRunResult(data=Character(name='Harry Potter', age=17))



#-------------------



# Example 2
# https://ai.pydantic.dev/examples/bank-support/#running-the-example

from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext


class DatabaseConn:
    """This is a fake database for example purposes.

    In reality, you'd be connecting to an external database
    (e.g. PostgreSQL) to get information about customers.
    """

    @classmethod
    async def customer_name(cls, *, id: int) -> str | None:
        if id == 123:
            return 'John'

    @classmethod
    async def customer_balance(cls, *, id: int, include_pending: bool) -> float:
        print("\n***id: ", id) # clm
        print("\n***include_pending: ", include_pending) # clm
        if id == 123 and include_pending:
            return 123.45
        else:
            raise ValueError('Customer not found')


@dataclass
class SupportDependencies:
    customer_id: int
    db: DatabaseConn


class SupportResult(BaseModel):
    support_advice: str = Field(description='Advice returned to the customer')
    block_card: bool = Field(description='Whether to block their card or not')
    risk: int = Field(description='Risk level of query', ge=0, le=10)


support_agent = Agent(
    model,
    deps_type=SupportDependencies,
    result_type=SupportResult,
    system_prompt=(
        'You are a support agent in our bank, give the '
        'customer support and judge the risk level of their query. '
        "Reply using the customer's name."
    ),
)


@support_agent.system_prompt
async def add_customer_name(ctx: RunContext[SupportDependencies]) -> str:
    customer_name = await ctx.deps.db.customer_name(id=ctx.deps.customer_id)
    print("\n*** Got customer_name: ", customer_name)
    return f"The customer's name is {customer_name!r}"


@support_agent.tool
async def customer_balance(
    ctx: RunContext[SupportDependencies], include_pending: bool
) -> str:
    """Returns the customer's current account balance."""
    balance = await ctx.deps.db.customer_balance(
        id=ctx.deps.customer_id,
        include_pending=include_pending,
    )
    return f'${balance:.2f}'


if __name__ == '__main__':
    deps = SupportDependencies(customer_id=123, db=DatabaseConn())
    result = support_agent.run_sync('What is my balance?', deps=deps)
    print(result.data)
    """
    # EXPECTED RESULT:
    support_advice='Hello John, your current account balance, including pending transactions, \
    is $123.45.' block_card=False risk=1
    """
    # Out[]: 2025MAR24
    """
    # FIRST REAL RESULT (This is not an error; the system worked correctly. The ValueError \
    # was raised by the program flow):
    Cell In[24], line 23, in DatabaseConn.customer_balance(cls, id, include_pending)
        21     return 123.45
        22 else:
    ---> 23     raise ValueError('Customer not found')

    ValueError: Customer not found
    """

    # SECOND TRY:
    result = support_agent.run_sync('What is my pending balance?', deps=deps)
    In [28]: print(result)
    # Out[]: 2025MAR24
    [GIN] 2025/03/24 - 04:22:19 | 200 |         1m10s |       127.0.0.1 | POST     "/v1/chat/completions"
    [GIN] 2025/03/24 - 04:22:59 | 200 |  40.00411266s |       127.0.0.1 | POST     "/v1/chat/completions"
    [GIN] 2025/03/24 - 04:23:35 | 200 | 35.921575886s |       127.0.0.1 | POST     "/v1/chat/completions"
    """
    # SECOND REAL RESULT:
    AgentRunResult(
    data=SupportResult(support_advice='Your pending balance is currently at $123.45.', 
    block_card=False, 
    risk=0))
    """



    result = support_agent.run_sync('I just lost my card!', deps=deps)
    print(result.data)
    """
    # EXPECTED RESULT:
    support_advice="I'm sorry to hear that, John. We are temporarily blocking your card to \
    prevent unauthorized transactions." block_card=True risk=8
    """
    # Out[]: 2025MAR24
    """
    # FIRST REAL RESULT:
    AgentRunResult(data=SupportResult(support_advice='John, please be cautious and monitor \
    your account. If you notice any unusual activities, contact us immediately.', 
    block_card=True, 
    risk=3))
    """
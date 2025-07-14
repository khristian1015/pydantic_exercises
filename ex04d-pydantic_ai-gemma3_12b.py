
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
    model_name = "gemma3:12b",
    base_url="http://localhost:11434/v1",
    api_key="ollama", # required, but unused
)

agent = Agent(
    model, 
    result_type=Character
)

result = agent.run_sync("Tell me about Harry Potter")
# Out[]: 2025MAR23
ModelHTTPError: status_code: 400, model_name: gemma3:12b, 
body: {'message': 'registry.ollama.ai/library/gemma3:12b does not support tools', 
       'type': 'api_error', 'param': None, 'code': None}


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
# Out[]: 2025MAR23
ModelHTTPError: status_code: 400, model_name: gemma3:12b, 
body: {'message': 'registry.ollama.ai/library/gemma3:12b does not support tools', 
       'type': 'api_error', 'param': None, 'code': None}

# NOT RUN
    print(result.data)
    """
    support_advice='Hello John, your current account balance, including pending transactions, \
    is $123.45.' block_card=False risk=1
    """

    result = support_agent.run_sync('I just lost my card!', deps=deps)
    print(result.data)
    """
    support_advice="I'm sorry to hear that, John. We are temporarily blocking your card to \
    prevent unauthorized transactions." block_card=True risk=8
    """

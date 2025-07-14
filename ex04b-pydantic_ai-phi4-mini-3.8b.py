
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
    model_name = "phi4-mini",
    base_url="http://localhost:11434/v1",
    api_key="ollama", # required, but unused
)

agent = Agent(
    model, 
    result_type=Character
)

result = agent.run_sync("Tell me about Harry Potter")
# Out[]: 2025MAR18
UnexpectedModelBehavior: Exceeded maximum retries (1) for result validation
# Out[]: 2025MAR23
UnexpectedModelBehavior: Exceeded maximum retries (1) for result validation
# Out[]: 2025MAR23
UnexpectedModelBehavior: Exceeded maximum retries (1) for result validation

# Changing prompt
result = agent.run_sync("The customer's name is John Doe, and he is 17 years old.")
# Out[]: 2025MAR23
UnexpectedModelBehavior: Exceeded maximum retries (1) for result validation


agent = Agent(
    model, 
    result_type=Character,
    system_prompt="You are an assistant that extracts relevant information from results"
)

# Changing prompt
result = agent.run_sync("Extract from: The customer's name is John Doe, and he is 17 years old.")
# Out[]: 2025MAR23
UnexpectedModelBehavior: Exceeded maximum retries (1) for result validation

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
    model, # Uses model definition from Example 1 , above
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
UnexpectedModelBehavior: Exceeded maximum retries (1) for result validation
# NOT RUN
    print(result.data)
    """
    support_advice='Hello John, your current account balance, including pending transactions, is $123.45.' block_card=False risk=1
    """

    result = support_agent.run_sync('I just lost my card!', deps=deps)
    print(result.data)
    """
    support_advice="I'm sorry to hear that, John. We are temporarily blocking your card to prevent unauthorized transactions." block_card=True risk=8
    """

# Part of error message (I collected it because it has a similar patter to instructor)
try:
--> 273     return await self.client.chat.completions.create(
    274         model=self._model_name,
    275         messages=openai_messages,
    276         n=1,
    277         parallel_tool_calls=model_settings.get('parallel_tool_calls', NOT_GIVEN),
    278         tools=tools or NOT_GIVEN,
    279         tool_choice=tool_choice or NOT_GIVEN,
    280         stream=stream,
    281         stream_options={'include_usage': True} if stream else NOT_GIVEN,
    282         max_tokens=model_settings.get('max_tokens', NOT_GIVEN),
    283         temperature=model_settings.get('temperature', NOT_GIVEN),
    284         top_p=model_settings.get('top_p', NOT_GIVEN),
    285         timeout=model_settings.get('timeout', NOT_GIVEN),
    286         seed=model_settings.get('seed', NOT_GIVEN),
    287         presence_penalty=model_settings.get('presence_penalty', NOT_GIVEN),
    288         frequency_penalty=model_settings.get('frequency_penalty', NOT_GIVEN),
    289         logit_bias=model_settings.get('logit_bias', NOT_GIVEN),
    290         reasoning_effort=model_settings.get('openai_reasoning_effort', NOT_GIVEN),
    291     )
    292 except APIStatusError as e:



validate_response_format(response_format)
-> 2000 return await self._post(
   2001     "/chat/completions",
   2002     body=await async_maybe_transform(
   2003         {
   2004             "messages": messages,
   2005             "model": model,
   2006             "audio": audio,
   2007             "frequency_penalty": frequency_penalty,
   2008             "function_call": function_call,
   2009             "functions": functions,
   2010             "logit_bias": logit_bias,
   2011             "logprobs": logprobs,
   2012             "max_completion_tokens": max_completion_tokens,
   2013             "max_tokens": max_tokens,
   2014             "metadata": metadata,
   2015             "modalities": modalities,
   2016             "n": n,
   2017             "parallel_tool_calls": parallel_tool_calls,
   2018             "prediction": prediction,
   2019             "presence_penalty": presence_penalty,
   2020             "reasoning_effort": reasoning_effort,
   2021             "response_format": response_format,
   2022             "seed": seed,
   2023             "service_tier": service_tier,
   2024             "stop": stop,
   2025             "store": store,
   2026             "stream": stream,
   2027             "stream_options": stream_options,
   2028             "temperature": temperature,
   2029             "tool_choice": tool_choice,
   2030             "tools": tools,
   2031             "top_logprobs": top_logprobs,
   2032             "top_p": top_p,
   2033             "user": user,
   2034             "web_search_options": web_search_options,
   2035         },
   2036         completion_create_params.CompletionCreateParams,
   2037     ),
   2038     options=make_request_options(
   2039         extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
   2040     ),
   2041     cast_to=ChatCompletion,
   2042     stream=stream or False,
   2043     stream_cls=AsyncStream[ChatCompletionChunk],
   2044 )


Links to save
https://medium.com/@jageenshukla/building-a-pydantic-agent-with-a-local-ollama-model-and-tool-creation-63dbf2bdc6ee

Google search: using pydantic ai with ollama

https://medium.com/@didierlacroix/pydantic-agents-and-ollama-part-1-a-recommendation-system-using-prompt-injection-for-context-7c0591ac537a

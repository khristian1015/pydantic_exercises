

ex01.py
-- Examples from Jason Liu's talk "Pydantic is all you need"

ex02-phi4-mini-3.8b.py
-- First example (run in lenovo Lap) from instructor page for tool function using Pydantic BaseModel and LLM = phi4-mini.
-- Example case: "Tell me about Harry Potter" / class Character (name, age)
-- Worked OK

ex03a-gemma3-12b.py
-- Same example as previous (w/instructor + pydantic), LLM model = gemma3-12b in PCDell7050
-- Example case: "Tell me about Harry Potter" / class Character (name, age)
-- OK

ex03b-gemma3-1b.py
-- Same example as previous (w/instructor + pydantic), LLM model = gemma3-1b in Lap HP Pavilion 14
-- Example case: "Tell me about Harry Potter" / class Character (name, age) - OK
-- Example case: Similar to Harry Potter, but it's a simple extraction - OK
-- Example case: More complex model: extract addresses - OK (second try)
-- OK but often it doesn't run during the first try.

ex03c...
-- Example with some sql pydantic formats but didn't work

ex04a-pydantic_ai-gem3-1b.py
-- Uses from pydantic_ai import Agent
-- Same example as previous (w/pydantic_ai only), LLM model = gemma3-1b in Lap HP Pavilion 14
-- Example case: "Tell me about Harry Potter" / class Character (name, age)
-- NOT OK: 'registry.ollama.ai/library/gemma3:1b does not support tools'

ex04b-pydantic_ai-phi4-mini-3.8b.py
-- Uses from pydantic_ai import Agent
-- Same example as previous (w/pydantic_ai only), LLM model = phi4-mini in Lap HP Pavilion 14
-- Example case: "Tell me about Harry Potter" / class Character (name, age) - NOT OK
-- Example case: Bank support  - NOT OK
-- NOT OK: UnexpectedModelBehavior: Exceeded maximum retries (1) for result validation

ex04c-pydantic_ai-llama3.2-3b.py
-- Uses from pydantic_ai import Agent
-- Same example as previous (w/pydantic_ai only), LLM model = llama3.2-3b in Lap HP Pavilion 14
-- Example case: "Tell me about Harry Potter" / class Character (name, age) - NOT OK
-- Example case: Bank support  - NOT RUN
-- NOT OK

ex04d-pydantic_ai-gemma3_12b.py
-- Uses from pydantic_ai import Agent
-- Same example as previous (w/pydantic_ai only), LLM model = gemma3-12b in Optiplex 7050
-- Example case: "Tell me about Harry Potter" / class Character (name, age) - NOT OK (gemma3:12b does not support tools)
-- Example case: Bank support  - NOT OK (gemma3:12b does not support tools)
-- NOT OK: 'registry.ollama.ai/library/gemma3:12b does not support tools'

ex04e-pydantic_ai-qwen2.5_14b.py
-- Uses from pydantic_ai import Agent
-- Same example as previous (w/pydantic_ai only), LLM model = qwen2.5:14b in Optiplex 7050
-- Example case: "Tell me about Harry Potter" / class Character (name, age) - OK
-- Example case: Bank support  - OK

ex05a-pydantic_ai-llama3.2-3b.py
-- Uses from pydantic_ai import Agent
-- Different example. No modeling of response, just plain question to LLM. 
-- LLM model = llama3.2-3b in Lap HP Pavilion 14
-- Example case: "What is the capital of France?" / no response_model
-- OK

ex05b-pydantic_ai-gemma3-1b.py
-- Uses from pydantic_ai import Agent
-- Same example as previous. No response modeling, just plain question to LLM
-- LLM model = gemma3-1b in Lap HP Pavilion 14
-- OK


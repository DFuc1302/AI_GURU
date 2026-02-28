import time
from llm_clients import call_llm

system_prompt = "You are a coding assistant."
user_prompt = "Write 50 lines of Python code."

start = time.time()
response = call_llm(system_prompt, user_prompt)
end = time.time()

print(response)
print("Time:", end - start)
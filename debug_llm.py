import time
from llm_clients import call_model

start = time.time()

response = call_model(
    model="qwen2.5-14b-instruct",
    messages=[{"role": "user", "content": "Write a Python function to compute factorial."}],
    temperature=0.2,
    max_tokens=300
)

end = time.time()

print(response)
print("Time:", end - start)
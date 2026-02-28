from llm_clients import call_llm_json

system = "You are strict."
user = "Return JSON with key 'answer' and value 42."

result = call_llm_json(system, user)

print(result)
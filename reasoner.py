# agents/reasoner.py

import json
from llm_clients import call_llm_json


def reasoner(input_data, temperature=0):

    if isinstance(input_data, dict):
        user_prompt = json.dumps(input_data, indent=2)
    else:
        user_prompt = str(input_data)

    system_prompt = """
You are a mathematical reasoning engine.

Solve the problem symbolically.
Provide clean final formula.
Provide short derivation steps.

Output strictly JSON:

{
  "formula": "mathematical expression",
  "derivation": "short reasoning steps"
}
"""

    result = call_llm_json(system_prompt, user_prompt, temperature=temperature)

    if not result:
        return None

    result.setdefault("formula", None)
    result.setdefault("derivation", None)

    return result
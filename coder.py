import json
import re
from llm_clients import call_llm


def extract_json(raw):

    if not raw:
        return None

    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        return None

    json_str = match.group()

    try:
        return json.loads(json_str)
    except Exception:
        return None


def coder(input_data, language="python"):

    if isinstance(input_data, dict):
        user_prompt = json.dumps(input_data, indent=2)
    else:
        user_prompt = str(input_data)

    system_prompt = f"""
You are a professional software engineer.

Task:
Generate complete runnable {language} code.

Rules:
- Return ONLY JSON
- No explanation
- No markdown
- Format:

{{
  "code": "complete runnable {language} code"
}}
"""

    raw = call_llm(system_prompt, user_prompt, temperature=0.2)

    result = extract_json(raw)

    if not result:
        print("❌ JSON extraction failed")
        print("RAW OUTPUT:\n", raw)
        return None

    if "code" not in result:
        print("❌ No code key found")
        print("RAW OUTPUT:\n", raw)
        return None

    return result
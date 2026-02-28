import requests
import json

# ============================================================
# CONFIG
# ============================================================

BASE_URL = "http://192.168.1.8:2805/v1/chat/completions"

# 🔥 Default model
MODEL = "qwen2.5-14b-instruct"
# MODEL = "DeepSeek-Coder-V2-Lite-Instruct"

TIMEOUT = 120


# ============================================================
# CORE LLM CALL
# ============================================================

def call_llm(system_prompt, user_prompt, max_tokens=1200, temperature=0, model=None):

    if model is None:
        model = MODEL

    # ------------------------------------------------------------
    # Force strict JSON behavior
    # ------------------------------------------------------------
    full_prompt = f"""
{system_prompt}

USER REQUEST:
{user_prompt}

CRITICAL INSTRUCTIONS:
- Return ONLY valid JSON
- Do NOT explain
- Do NOT add markdown
- Do NOT wrap with ```json
- Output must start with {{
"""

    payload = {
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": [
            {
                "role": "user",
                "content": full_prompt
            }
        ],
        "stop": ["```"]
    }

    try:
        response = requests.post(BASE_URL, json=payload, timeout=TIMEOUT)

        if response.status_code != 200:
            raise RuntimeError(f"HTTP {response.status_code}: {response.text}")

        data = response.json()
        content = data["choices"][0]["message"]["content"]

        # --------------------------------------------------------
        # Clean accidental markdown
        # --------------------------------------------------------
        content = content.strip()

        if content.startswith("```"):
            content = content.replace("```json", "")
            content = content.replace("```", "")
            content = content.strip()

        return content

    except Exception as e:
        print("🔥 LLM ERROR:", e)
        return None


# ============================================================
# SAFE JSON PARSER
# ============================================================

def call_llm_json(system_prompt, user_prompt, max_tokens=1200, temperature=0, model=None):

    raw = call_llm(system_prompt, user_prompt, max_tokens, temperature, model)

    if not raw:
        return None

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print("⚠️ JSON PARSE FAILED")
        print("RAW OUTPUT:\n", raw)
        return None


# ============================================================
# SIMPLE RAW CALL (for benchmark / quick test)
# ============================================================

def call_model(model, messages, temperature=0, max_tokens=512):
    """
    Dùng cho test nhanh không ép JSON
    """

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    try:
        response = requests.post(BASE_URL, json=payload, timeout=TIMEOUT)

        if response.status_code != 200:
            raise RuntimeError(f"HTTP {response.status_code}: {response.text}")

        data = response.json()
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print("🔥 RAW CALL ERROR:", e)
        return None
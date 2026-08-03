from llm_clients import call_llm


PLANNER_PROMPT = """
You are a problem analysis engine.

Rules:
- Do NOT write code.
- Do NOT include explanations.
- Output only a concise plan.
- Maximum 5 bullet points.

If it is a math problem:
- Identify the function
- Identify what to compute
- State the mathematical operation

If it is a coding problem:
- Describe required functionality
- Mention edge cases briefly
"""


def planner(problem: str):

    prompt = f"""
Problem:
{problem}

Generate structured plan only.
"""

    response = call_llm(
        system_prompt=PLANNER_PROMPT,
        user_prompt=prompt
    )

    return response.strip()

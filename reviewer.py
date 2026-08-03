from llm_clients import call_llm


SUPPORTED_LANGUAGES = [
    "python",
    "cpp",
    "java",
    "javascript",
    "html"
]


def reviewer(code: str, language: str = "python") -> str:
    """
    Review generated code and decide whether it is approved.
    If issues exist, suggest improvements.
    """

    if not code:
        return None

    language = language.lower()

    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language: {language}")

    system_prompt = f'''
        You are a strict senior code reviewer.

If the code is correct:
Respond with:
APPROVED

If incorrect:
Explain issues clearly.
Focus on:
- Logical errors
- Edge cases
- Runtime issues
- Performance problems

Be concise.
'''

    return call_llm(system_prompt, code)

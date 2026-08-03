from llm_clients import call_llm


SUPPORTED_LANGUAGES = [
    "python",
    "cpp",
    "java",
    "javascript",
    "html"
]


def tester(code: str, language: str = "python") -> str:
    """
    Generate test cases for the given code.
    """

    if not code:
        return None

    language = language.lower()

    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language: {language}")

    system_prompt = f'''
Generate strong test cases including:
- Normal cases
- Edge cases
- Stress cases

Return plain text.
'''

    return call_llm(system_prompt, code)

import subprocess
import tempfile
import os
import re
import sys


def clean_code_block(code: str):
    """
    Extract pure code from LLM output.
    Removes explanation text and markdown.
    Also fixes escaped newline issues.
    """

    if not code:
        return ""

    # 🔥 Convert escaped newlines to real newlines
    try:
        code = code.encode().decode("unicode_escape")
    except Exception:
        pass

    # Extract ```python block if exists
    match = re.search(r"```python(.*?)```", code, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Remove generic markdown fences
    code = re.sub(r"```.*?```", "", code, flags=re.DOTALL)

    lines = code.splitlines()
    cleaned_lines = []

    for line in lines:
        stripped = line.strip()

        # Skip obvious explanation lines
        if stripped.startswith(("The ", "This ", "Here ", "Sure", "In ")):
            continue

        # Skip standalone language labels
        if stripped.lower() in ["python", "java", "cpp", "c++", "javascript"]:
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()


def run_code_safely(code, language):
    try:
        with tempfile.TemporaryDirectory() as tmpdir:

            # 🔥 Always clean + fix code
            code = clean_code_block(code)

            if language == "python":
                file_path = os.path.join(tmpdir, "main.py")

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(code)

                result = subprocess.run(
                    [sys.executable, file_path],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

            elif language == "cpp":
                source_path = os.path.join(tmpdir, "main.cpp")
                binary_path = os.path.join(tmpdir, "main")

                with open(source_path, "w", encoding="utf-8") as f:
                    f.write(code)

                compile_result = subprocess.run(
                    ["g++", source_path, "-o", binary_path],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                if compile_result.returncode != 0:
                    return {
                        "stdout": "",
                        "stderr": compile_result.stderr,
                        "returncode": compile_result.returncode,
                        "executed_code": code
                    }

                result = subprocess.run(
                    [binary_path],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

            elif language == "java":
                source_path = os.path.join(tmpdir, "Main.java")

                with open(source_path, "w", encoding="utf-8") as f:
                    f.write(code)

                compile_result = subprocess.run(
                    ["javac", source_path],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                if compile_result.returncode != 0:
                    return {
                        "stdout": "",
                        "stderr": compile_result.stderr,
                        "returncode": compile_result.returncode,
                        "executed_code": code
                    }

                result = subprocess.run(
                    ["java", "-cp", tmpdir, "Main"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

            elif language == "javascript":
                file_path = os.path.join(tmpdir, "main.js")

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(code)

                result = subprocess.run(
                    ["node", file_path],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

            else:
                return {
                    "stdout": "",
                    "stderr": "Unsupported language",
                    "returncode": 1,
                    "executed_code": code
                }

            # 🔥 Warning if no output
            warning = ""
            if result.returncode == 0 and result.stdout.strip() == "":
                warning = "Code executed successfully but produced no output."

            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "warning": warning,
                "executed_code": code
            }

    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": "Execution timed out",
            "returncode": -1,
            "executed_code": code
        }

    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "returncode": -1,
            "executed_code": code
        }

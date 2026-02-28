from agents.planner import planner
from agents.coder import coder
from agents.reviewer import reviewer
from agents.tester import tester
from symbolic_verifier import verify_formula
from sandbox import run_code_safely


def run_multi_agent(problem, language="python"):

    # ============================================================
    # 1️⃣ Planner
    # ============================================================
    plan = planner(problem)

    if not plan:
        return {"error": "Planner failed.", "problem": problem}

    # ============================================================
# 2️⃣ Code Generation
# ============================================================

    code = coder(problem, language=language)

    if not code:
        return {"error": "Code generation failed."}

    formula = None
    derivation = None

    # ============================================================
    # HYBRID MODE HANDLING
    # ============================================================
    if not code and formula:
        # Math-only mode
        verification = verify_formula(problem, formula) if formula else None

        return {
            "plan": plan,
            "formula": formula,
            "derivation": derivation,
            "verification": verification,
            "mode": "math-only"
        }

    if not code:
        return {"plan": plan, "error": "No code returned from coder."}

    # ============================================================
    # 3️⃣ Symbolic Verification (if formula exists)
    # ============================================================
    formula_verification = None

    if formula:
        formula_verification = verify_formula(problem, formula)

        if not formula_verification.get("valid", False):
            return {
                "plan": plan,
                "formula": formula,
                "verification": formula_verification,
                "error": "Formula verification failed."
            }

    # ============================================================
    # 4️⃣ Reviewer Loop
    # ============================================================
    max_review_round = 2
    review = None

    for _ in range(max_review_round):

        review = reviewer(code, language=language)

        if isinstance(review, str) and "APPROVED" in review.upper():
            break

        # regenerate with feedback
        coder_retry = coder(review, language=language)

        if not coder_retry or not isinstance(coder_retry, dict):
            return {"plan": plan, "review": review, "error": "Code regeneration failed."}

        code = coder_retry.get("code")
        formula = coder_retry.get("formula")

        if not code:
            return {"plan": plan, "review": review, "error": "No regenerated code."}

    # ============================================================
    # 5️⃣ Self-Fix Sandbox Loop
    # ============================================================
    max_retry = 3
    sandbox_result = None

    for _ in range(max_retry):

        sandbox_result = run_code_safely(code, language)

        if sandbox_result.get("returncode", 1) == 0:
            break

        feedback = f"""
        The following code failed to execute:

        {code}

        Error:
        {sandbox_result.get('stderr')}

        Please fix the code.
        """

        coder_retry = coder(feedback, language=language)

        if not coder_retry:
            break

        code = coder_retry.get("code")

    # ============================================================
    # 6️⃣ Testing Phase (if exists)
    # ============================================================
    try:
        tests = tester(code, language=language)
    except Exception as e:
        tests = {"error": str(e)}

    return {
        "plan": plan,
        "formula": formula,
        "derivation": derivation,
        "verification": formula_verification,
        "code": code,
        "review": review,
        "tests": tests,
        "sandbox": sandbox_result,
        "mode": "hybrid"
    }
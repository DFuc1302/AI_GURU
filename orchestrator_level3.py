from agents.planner import planner
from agents.coder import coder
from agents.reviewer import reviewer
from agents.reasoner import reasoner

from voting import voting_engine
from symbolic_verifier import verify_formula
from numeric_verifier import numeric_verify
from sandbox import run_code_safely
from confidence import compute_confidence


def run_pipeline(problem, language="python"):

    # 1️⃣ Planner
    plan = planner(problem)
    if not plan:
        return {"error": "Planner failed"}

    # 2️⃣ Dual Reasoning
    r1 = reasoner(plan, temperature=0)
    r2 = reasoner(plan, temperature=0.5)

    chosen_reasoning, dual_agreement = voting_engine(r1, r2)

    if not chosen_reasoning:
        return {"error": "Reasoning failed"}

    formula = chosen_reasoning.get("formula")
    derivation = chosen_reasoning.get("derivation")

    # 3️⃣ Verification
    symbolic_verification = verify_formula(problem, formula) if formula else {"valid": False}
    symbolic_pass = symbolic_verification.get("valid", False)

    numeric_pass = numeric_verify(formula) if formula else False

    # Retry if failed
    if not symbolic_pass or not numeric_pass:
        r_retry = reasoner(plan, temperature=0.7)

        formula = r_retry.get("formula")
        derivation = r_retry.get("derivation")

        symbolic_verification = verify_formula(problem, formula) if formula else {"valid": False}
        symbolic_pass = symbolic_verification.get("valid", False)

        numeric_pass = numeric_verify(formula) if formula else False

    # 4️⃣ Code Generation (Hybrid aware)
    coder_input = {
        "problem": problem,
        "formula": formula,
        "instruction": "Write simple code that prints the derivative result only."
    }

    coder_result = coder(coder_input, language=language)

    if not coder_result:
        return {"error": "Code generation failed"}

    code = coder_result.get("code")

    if not code:
        return {"error": "Empty code returned"}

    # 5️⃣ Sandbox
    sandbox_result = run_code_safely(code, language)
    sandbox_success = sandbox_result.get("returncode", 1) == 0

    # 6️⃣ Review
    review = reviewer(code, language=language)

    if isinstance(review, str):
        reviewer_approved = "APPROVED" in review.upper()
    else:
        reviewer_approved = review.get("approved", False)

    # 7️⃣ Confidence
    confidence = compute_confidence(
        dual_agreement,
        symbolic_pass,
        numeric_pass,
        sandbox_success,
        reviewer_approved
    )

    return {
        "plan": plan,
        "formula": formula,
        "derivation": derivation,
        "symbolic_verification": symbolic_verification,
        "numeric_pass": numeric_pass,
        "code": code,
        "sandbox": sandbox_result,
        "confidence": confidence
    }
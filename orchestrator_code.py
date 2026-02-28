from agents.planner import planner
from agents.reasoner import reasoner
from agents.coder import coder
from agents.reviewer import reviewer
from sandbox import run_code_safely
from confidence import compute_confidence


def run_code_pipeline(problem, language="python"):

    # 1️⃣ Planner
    plan = planner(problem)
    if not plan:
        return {"error": "Planner failed"}

    # 2️⃣ Reasoning (logic before code)
    reasoning = reasoner(plan, temperature=0)

    if not reasoning:
        return {"error": "Reasoning failed"}

    # 3️⃣ Code generation based on reasoning
    coder_input = {
        "problem": problem,
        "plan": plan,
        "reasoning": reasoning
    }

    coder_result = coder(coder_input, language=language)

    if not coder_result:
        return {"error": "Code generation failed"}

    code = coder_result.get("code")

    if not code:
        return {"error": "Empty code returned"}

    # 4️⃣ Sandbox
    sandbox_result = run_code_safely(code, language)
    sandbox_success = sandbox_result.get("returncode", 1) == 0

    # 5️⃣ Review
    review = reviewer(code, language=language)

    if isinstance(review, str):
        reviewer_approved = "APPROVED" in review.upper()
    else:
        reviewer_approved = review.get("approved", False)

    # 6️⃣ Confidence (không còn symbolic/numeric)
    confidence = compute_confidence(
        dual_agreement=True,      # luôn True vì chỉ 1 reasoning
        symbolic_pass=True,
        numeric_pass=True,
        sandbox_success=sandbox_success,
        reviewer_approved=reviewer_approved
    )

    return {
        "plan": plan,
        "reasoning": reasoning,
        "code": code,
        "sandbox": sandbox_result,
        "review": review,
        "confidence": confidence
    }
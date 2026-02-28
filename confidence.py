# core/confidence.py

def compute_confidence(
    dual_agreement,
    symbolic_pass,
    numeric_pass,
    sandbox_success,
    reviewer_approved
):

    score = 0

    if dual_agreement:
        score += 0.25

    if symbolic_pass:
        score += 0.30

    if numeric_pass:
        score += 0.20

    if sandbox_success:
        score += 0.15

    if reviewer_approved:
        score += 0.10

    return round(score, 3)
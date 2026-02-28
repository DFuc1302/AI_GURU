from sympy import symbols, sympify, diff, simplify
import re


# ------------------------------------------------------------
# Extract expression from problem
# ------------------------------------------------------------
def extract_expression(problem):
    match = re.search(r"=\s*([^,]+)", problem)
    if not match:
        return None
    return match.group(1).strip()


# ------------------------------------------------------------
# Detect differentiation variable
# ------------------------------------------------------------
def detect_variable(expr_str):
    vars_found = re.findall(r"[a-zA-Z]", expr_str)
    if not vars_found:
        return "x"
    return vars_found[0]


# ------------------------------------------------------------
# Clean model formula before verification
# ------------------------------------------------------------
def clean_formula(formula):

    if not formula:
        return None

    formula = formula.strip()

    # Remove left side of '=' if exists
    if "=" in formula:
        formula = formula.split("=")[-1]

    formula = formula.strip().strip('"').strip("'")

    # 🚫 Reject code-like expressions
    forbidden_patterns = [
        "diff",
        "sp.",
        ".diff",
        "Derivative",
        "lambda",
        "def"
    ]

    for pattern in forbidden_patterns:
        if pattern in formula:
            return None

    return formula.strip()



# ------------------------------------------------------------
# Main Verification
# ------------------------------------------------------------
def verify_formula(problem, formula):

    try:
        expr_str = extract_expression(problem)
        if not expr_str:
            return {"valid": False, "error": "No expression found."}

        var_name = detect_variable(expr_str)
        var = symbols(var_name)

        # Parse original expression
        expr = sympify(expr_str.replace("^", "**"))
        true_derivative = diff(expr, var)

        # 🔥 Clean formula from model
        formula_clean = clean_formula(formula)

        if not formula_clean:
            return {
                "valid": False,
                "error": "Formula contains invalid or code-like expression."
            }

        formula_expr = sympify(formula_clean.replace("^", "**"))

        # 🔥 Compare symbolically instead of string compare
        is_valid = simplify(true_derivative - formula_expr) == 0

        return {
            "valid": bool(is_valid),
            "true_derivative": str(true_derivative)
        }

    except Exception as e:
        return {
            "valid": False,
            "error": str(e)
        }

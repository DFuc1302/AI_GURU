# agents/problem_analyzer.py

import re

def detect_problem_type(problem):
    """
    Detect whether problem is mathematical.
    """

    math_patterns = [
        r"=",
        r"\^",
        r"derivative",
        r"d/d",
        r"marginal",
        r"integral",
        r"function"
    ]

    for pattern in math_patterns:
        if re.search(pattern, problem, re.IGNORECASE):
            return "math"

    return "code"

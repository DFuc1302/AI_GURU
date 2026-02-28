# numeric_verifier.py

import sympy as sp
import random


def numeric_verify(formula_str, variable="x", trials=5, tol=1e-6):

    if not formula_str:
        return False

    try:
        x = sp.symbols(variable)
        expr = sp.sympify(formula_str.replace("^", "**"))
        f = sp.lambdify(x, expr, "math")

        for _ in range(trials):
            val = random.uniform(-5, 5)
            result = f(val)

            if result is None:
                return False

            if isinstance(result, complex):
                return False

        return True

    except Exception:
        return False
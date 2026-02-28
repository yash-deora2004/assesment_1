"""
Calculator Tool — Sympy-based math calculator for the Solver Agent.
"""

import math
import re
from typing import Dict, Any

import sympy
from sympy import (
    symbols, sympify, solve, diff, integrate, limit, simplify,
    expand, factor, Matrix, det, Rational, oo, pi, E, I,
    sin, cos, tan, log, exp, sqrt, Abs,
)
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)

TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)


def safe_parse(expression: str) -> sympy.Expr:
    """Safely parse a math expression string into a sympy expression."""
    # Clean the expression
    expr_str = expression.strip()
    expr_str = expr_str.replace("^", "**")
    expr_str = expr_str.replace("ln(", "log(")

    try:
        return parse_expr(expr_str, transformations=TRANSFORMATIONS)
    except Exception as e:
        raise ValueError(f"Could not parse expression '{expression}': {e}")


def evaluate_expression(expression: str) -> Dict[str, Any]:
    """Evaluate a mathematical expression and return the result."""
    try:
        expr = safe_parse(expression)
        result = simplify(expr)
        return {
            "success": True,
            "input": expression,
            "result": str(result),
            "numeric": float(result) if result.is_number else None,
        }
    except Exception as e:
        return {"success": False, "input": expression, "error": str(e)}


def solve_equation(equation_str: str, variable: str = "x") -> Dict[str, Any]:
    """Solve an equation. Use '=' for equations or assume '= 0' if no '='."""
    try:
        var = symbols(variable)

        if "=" in equation_str:
            lhs_str, rhs_str = equation_str.split("=", 1)
            lhs = safe_parse(lhs_str)
            rhs = safe_parse(rhs_str)
            equation = lhs - rhs
        else:
            equation = safe_parse(equation_str)

        solutions = solve(equation, var)
        return {
            "success": True,
            "input": equation_str,
            "variable": variable,
            "solutions": [str(s) for s in solutions],
            "num_solutions": len(solutions),
        }
    except Exception as e:
        return {"success": False, "input": equation_str, "error": str(e)}


def compute_derivative(expression: str, variable: str = "x", order: int = 1) -> Dict[str, Any]:
    """Compute the derivative of an expression."""
    try:
        var = symbols(variable)
        expr = safe_parse(expression)
        result = diff(expr, var, order)
        return {
            "success": True,
            "input": expression,
            "variable": variable,
            "order": order,
            "result": str(simplify(result)),
        }
    except Exception as e:
        return {"success": False, "input": expression, "error": str(e)}


def compute_integral(expression: str, variable: str = "x",
                     lower: str = None, upper: str = None) -> Dict[str, Any]:
    """Compute definite or indefinite integral."""
    try:
        var = symbols(variable)
        expr = safe_parse(expression)

        if lower is not None and upper is not None:
            a = safe_parse(lower)
            b = safe_parse(upper)
            result = integrate(expr, (var, a, b))
            return {
                "success": True,
                "input": expression,
                "type": "definite",
                "bounds": [str(a), str(b)],
                "result": str(simplify(result)),
                "numeric": float(result) if result.is_number else None,
            }
        else:
            result = integrate(expr, var)
            return {
                "success": True,
                "input": expression,
                "type": "indefinite",
                "result": str(simplify(result)) + " + C",
            }
    except Exception as e:
        return {"success": False, "input": expression, "error": str(e)}


def compute_limit(expression: str, variable: str = "x",
                  point: str = "0", direction: str = "") -> Dict[str, Any]:
    """Compute the limit of an expression."""
    try:
        var = symbols(variable)
        expr = safe_parse(expression)
        pt = safe_parse(point) if point != "oo" else oo

        kwargs = {}
        if direction == "+":
            kwargs["dir"] = "+"
        elif direction == "-":
            kwargs["dir"] = "-"

        result = limit(expr, var, pt, **kwargs)
        return {
            "success": True,
            "input": expression,
            "variable": variable,
            "point": point,
            "result": str(result),
        }
    except Exception as e:
        return {"success": False, "input": expression, "error": str(e)}


def compute_determinant(matrix_list: list) -> Dict[str, Any]:
    """Compute the determinant of a matrix given as list of lists."""
    try:
        M = Matrix(matrix_list)
        result = det(M)
        return {
            "success": True,
            "matrix": str(M.tolist()),
            "determinant": str(result),
            "numeric": float(result) if result.is_number else None,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def matrix_inverse(matrix_list: list) -> Dict[str, Any]:
    """Compute the inverse of a matrix."""
    try:
        M = Matrix(matrix_list)
        d = det(M)
        if d == 0:
            return {"success": False, "error": "Matrix is singular (det = 0), inverse does not exist."}
        inv = M.inv()
        return {
            "success": True,
            "matrix": str(M.tolist()),
            "inverse": str(inv.tolist()),
            "determinant": str(d),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def compute_probability(n: int, r: int, prob_type: str = "combination") -> Dict[str, Any]:
    """Compute combinatorial quantities."""
    try:
        if prob_type == "combination":
            result = math.comb(n, r)
            label = f"C({n},{r})"
        elif prob_type == "permutation":
            result = math.perm(n, r)
            label = f"P({n},{r})"
        elif prob_type == "factorial":
            result = math.factorial(n)
            label = f"{n}!"
        else:
            return {"success": False, "error": f"Unknown type: {prob_type}"}

        return {"success": True, "type": prob_type, "expression": label, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


def run_calculation(operation: str, **kwargs) -> Dict[str, Any]:
    """
    Unified entry point for calculator operations.

    Supported operations:
        evaluate, solve, derivative, integral, limit,
        determinant, inverse, probability
    """
    dispatch = {
        "evaluate": lambda: evaluate_expression(kwargs.get("expression", "")),
        "solve": lambda: solve_equation(
            kwargs.get("equation", ""), kwargs.get("variable", "x")
        ),
        "derivative": lambda: compute_derivative(
            kwargs.get("expression", ""), kwargs.get("variable", "x"),
            kwargs.get("order", 1)
        ),
        "integral": lambda: compute_integral(
            kwargs.get("expression", ""), kwargs.get("variable", "x"),
            kwargs.get("lower"), kwargs.get("upper")
        ),
        "limit": lambda: compute_limit(
            kwargs.get("expression", ""), kwargs.get("variable", "x"),
            kwargs.get("point", "0"), kwargs.get("direction", "")
        ),
        "determinant": lambda: compute_determinant(kwargs.get("matrix", [])),
        "inverse": lambda: matrix_inverse(kwargs.get("matrix", [])),
        "probability": lambda: compute_probability(
            kwargs.get("n", 0), kwargs.get("r", 0),
            kwargs.get("prob_type", "combination")
        ),
    }

    if operation not in dispatch:
        return {"success": False, "error": f"Unknown operation: {operation}. Supported: {list(dispatch.keys())}"}

    return dispatch[operation]()

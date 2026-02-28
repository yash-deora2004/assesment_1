"""Tests for the Calculator Tool."""

import unittest
from tools.calculator import (
    evaluate_expression,
    solve_equation,
    compute_derivative,
    compute_integral,
    compute_limit,
    compute_determinant,
    compute_probability,
    run_calculation,
)


class TestCalculator(unittest.TestCase):
    """Test cases for the sympy calculator tool."""

    def test_evaluate_expression(self):
        """Test basic expression evaluation."""
        result = evaluate_expression("2 + 3 * 4")
        self.assertTrue(result["success"])
        self.assertEqual(result["numeric"], 14.0)

    def test_evaluate_with_powers(self):
        """Test expression with exponents."""
        result = evaluate_expression("2^10")
        self.assertTrue(result["success"])
        self.assertEqual(result["numeric"], 1024.0)

    def test_solve_quadratic(self):
        """Test solving quadratic equation."""
        result = solve_equation("x**2 - 5*x + 6 = 0")
        self.assertTrue(result["success"])
        self.assertEqual(result["num_solutions"], 2)
        solutions = sorted([str(s) for s in result["solutions"]])
        self.assertIn("2", solutions)
        self.assertIn("3", solutions)

    def test_solve_linear(self):
        """Test solving linear equation."""
        result = solve_equation("2*x + 3 = 7")
        self.assertTrue(result["success"])
        self.assertIn("2", result["solutions"])

    def test_derivative_polynomial(self):
        """Test differentiation of polynomial."""
        result = compute_derivative("x**3 + 2*x**2 - 5*x + 1")
        self.assertTrue(result["success"])
        self.assertIn("3*x**2", result["result"])

    def test_derivative_trig(self):
        """Test differentiation of trig function."""
        result = compute_derivative("sin(x)")
        self.assertTrue(result["success"])
        self.assertEqual(result["result"], "cos(x)")

    def test_integral_polynomial(self):
        """Test integration of polynomial."""
        result = compute_integral("3*x**2", "x")
        self.assertTrue(result["success"])
        self.assertIn("x**3", result["result"])

    def test_definite_integral(self):
        """Test definite integral."""
        result = compute_integral("x**2", "x", "0", "1")
        self.assertTrue(result["success"])
        self.assertAlmostEqual(result["numeric"], 1/3, places=5)

    def test_limit_standard(self):
        """Test standard limit sin(x)/x as x→0."""
        result = compute_limit("sin(x)/x", "x", "0")
        self.assertTrue(result["success"])
        self.assertEqual(result["result"], "1")

    def test_determinant_2x2(self):
        """Test 2x2 determinant."""
        result = compute_determinant([[1, 2], [3, 4]])
        self.assertTrue(result["success"])
        self.assertEqual(result["numeric"], -2.0)

    def test_determinant_3x3(self):
        """Test 3x3 determinant."""
        result = compute_determinant([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        self.assertTrue(result["success"])
        self.assertEqual(result["numeric"], 1.0)

    def test_probability_combination(self):
        """Test combination calculation."""
        result = compute_probability(10, 3, "combination")
        self.assertTrue(result["success"])
        self.assertEqual(result["result"], 120)

    def test_probability_permutation(self):
        """Test permutation calculation."""
        result = compute_probability(5, 3, "permutation")
        self.assertTrue(result["success"])
        self.assertEqual(result["result"], 60)

    def test_run_calculation_dispatch(self):
        """Test the unified run_calculation dispatcher."""
        result = run_calculation("evaluate", expression="1 + 1")
        self.assertTrue(result["success"])
        self.assertEqual(result["numeric"], 2.0)

    def test_run_calculation_unknown_op(self):
        """Test unknown operation."""
        result = run_calculation("unknown_op")
        self.assertFalse(result["success"])


if __name__ == "__main__":
    unittest.main()

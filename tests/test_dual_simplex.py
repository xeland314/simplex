from abc import ABC, abstractmethod
from decimal import Decimal
import unittest
import numpy as np

from algorithms.dual_simplex import DualSimplex

class TestDualSimplexBase(ABC):

    dual_simplex = None

    def setUp(self):
        """
        An optimization problem is defined with dual simplex.
        """

    def test_check_optimal_values(self):
        """
        The solutions of the system are checked.
        """
        solutions = self.get_solutions()
        solution, optimal_value = self.dual_simplex.solve()
        assert solution is not None, "No solution found"
        for i, value in enumerate(solution):
            var_name = f"x{i+1}"
            expected = solutions.get(var_name, 0)
            assert abs(value - float(expected)) < 1e-6, (
                f"Variable {var_name}: expected {expected}, got {value}"
            )
        expected_opt = self.get_optimal_value()
        assert abs(optimal_value - float(expected_opt)) < 1e-6, (
            f"Optimal value: expected {expected_opt}, got {optimal_value}"
        )

    @abstractmethod
    def get_solutions(self) -> dict[str, Decimal]:
        """
        Expected solutions.
        """

    @abstractmethod
    def get_optimal_value(self) -> Decimal:
        """
        Expected optimal value.
        """

class TestDualSimplex1(TestDualSimplexBase, unittest.TestCase):

    def setUp(self):
        c = [2, 1, -3, 5]
        A = [
            [1, 2, 2, 4],
            [2, -1, 1, 2],
            [4, -2, 1, -1]
        ]
        b = [40, 8, 10]
        self.dual_simplex = DualSimplex(c, A, b, maximize=True)

    def get_solutions(self) -> dict[str, Decimal]:
        return {
            "x1": Decimal("0"),
            "x2": Decimal("6"),
            "x3": Decimal("0"),
            "x4": Decimal("7")
        }

    def get_optimal_value(self) -> Decimal:
        return Decimal("41")

class TestDualSimplex2(TestDualSimplexBase, unittest.TestCase):
    """Test case with primal infeasible initial solution (negative b values)."""

    def setUp(self):
        c = [3, 2]
        A = [
            [1, 1],
            [2, -1]
        ]
        b = [10, -5]
        self.dual_simplex = DualSimplex(c, A, b, maximize=True)

    def get_solutions(self) -> dict[str, Decimal]:
        return {
            "x1": Decimal('1.6666666666666667'),
            "x2": Decimal('8.3333333333333339')
        }

    def get_optimal_value(self) -> Decimal:
        return Decimal('21.6666666666666667')

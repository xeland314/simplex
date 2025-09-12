from abc import ABC, abstractmethod
from decimal import Decimal
import unittest

from advanced_simplex import Simplex
from functions import AlgebraicExpression, ObjectiveFunction

class TestSimplexBase(ABC):

    simplex = Simplex()

    def setUp(self):
        """
        An optimization problem is defined with simplex.
        """

    def test_check_optimal_values(self):
        """
        The solutions of the system are checked.
        """
        solutions = self.get_solutions()
        for variable, value in self.simplex.optimal_values:
            # Use plain assert -> works in pytest and unittest
            assert solutions[variable] == value, (
                f"Variable {variable}: expected {solutions[variable]}, got {value}"
            )

    @abstractmethod
    def get_solutions(self) -> dict[str, Decimal]:
        """
        PHPSimplex is an online tool to solve linear programming
        problems using the simplex method.
        Its use is free of charge.

        - Link: http://www.phpsimplex.com/simplex/simplex.htm?l=en
        """

class TestSimplex1(TestSimplexBase, unittest.TestCase):

    def setUp(self):
        self.simplex = Simplex(
            num_variables=6,
            objective_function=ObjectiveFunction("z = 5x1 + 4x2 + 0s1 + 0s2 + 0s3 + 0s4"),
            method=Simplex.MAXIMIZE,
            constraints=[
                AlgebraicExpression("6x1 + 4x2 + s1 = 24"),
                AlgebraicExpression("x1 + 2x2 + s2 = 6"),
                AlgebraicExpression("-x1 + x2 + s3 = 1"),
                AlgebraicExpression("x2 + s4 = 2")
            ]
        )
        self.simplex.solve_problem()
        self.simplex.show_results()

    def get_solutions(self):
        return {
            "z": Decimal("21"),
            "x1": Decimal("3"),
            "x2": Decimal("1.5"),
            "s1": Decimal("0"),
            "s2": Decimal("0"),
            "s3": Decimal("2.5"),
            "s4": Decimal("0.5")
        }

class TestSimplex2(TestSimplexBase, unittest.TestCase):

    def setUp(self):
        self.simplex = Simplex(
            num_variables=4,
            objective_function=ObjectiveFunction("z = 2x1 + x2 - 3x3 + 5x4"),
            method=Simplex.MAXIMIZE,
            constraints=[
                AlgebraicExpression("x1 + 2x2 + 2x3 + 4x4 <= 40"),
                AlgebraicExpression("2x1 - x2 + x3 + 2x4 <= 8"),
                AlgebraicExpression("4x1 - 2x2 + x3 - x4 <= 10"),
            ]
        )
        self.simplex.solve_problem()

    def get_solutions(self):
        return {
            "z": Decimal("41"),
            "x1": Decimal("0"),
            "x2": Decimal("6"),
            "x3": Decimal("0"),
            "x4": Decimal("7")
        }


class TestSimplex2_1(TestSimplex2):

    def get_solutions(self):
        self.simplex.objective_function = ObjectiveFunction(
            "z = 8x1 + 6x2 + 3x3 - 2x4"
        )
        self.simplex.solve_problem()
        return {
            "z": Decimal("170"),
            "x1": Decimal("10"),
            "x2": Decimal("15"),
            "x3": Decimal("0"),
            "x4": Decimal("0")
        }

class TestSimplex2_2(TestSimplex2):

    def get_solutions(self):
        self.simplex.objective_function = ObjectiveFunction(
            "z = 3x1 - x2 + 3x3 + 4x4"
        )
        self.simplex.solve_problem()
        return {
            "z": Decimal("36"),
            "x1": Decimal("0"),
            "x2": Decimal("6"),
            "x3": Decimal("14"),
            "x4": Decimal("0")
        }

class TestSimplex2_3(TestSimplex2):

    def get_solutions(self):
        self.simplex.objective_function = ObjectiveFunction(
            "z = 5x1 - 4x2 + 6x3 - 8x4"
        )
        self.simplex.method = self.simplex.MINIMIZE
        self.simplex.solve_problem()
        return {
            "z": Decimal("-80"),
            "x1": Decimal("0"),
            "x2": Decimal("6"),
            "x3": Decimal("0"),
            "x4": Decimal("7")
        }

class TestSimplex3(TestSimplexBase, unittest.TestCase):

    def setUp(self):
        self.simplex = Simplex(
            num_variables=4,
            objective_function=ObjectiveFunction("z = x1+0*x2+0*x3+0*x4"),
            method=Simplex.MAXIMIZE,
            constraints=[
                AlgebraicExpression("5*x1 + x2 = 4"),
                AlgebraicExpression("6*x1 + x3 = 8"),
                AlgebraicExpression("3*x1 + x4 = 3"),
            ]
        )
        self.simplex.solve_problem()

    def get_solutions(self):
        return {
            "z": Decimal("0.8"),
            "x1": Decimal("0.8"),
            "x2": Decimal("0"),
            "x3": Decimal("3.2"),
            "x4": Decimal("0.6")
        }

class TestSimplex3_1(TestSimplexBase, unittest.TestCase):

    def setUp(self):
        self.simplex = Simplex(
            num_variables=4,
            objective_function=ObjectiveFunction("z = x1"),
            method=Simplex.MAXIMIZE,
            constraints=[
                AlgebraicExpression("5*x1 + s1 = 4"),
                AlgebraicExpression("6*x1 + s2 = 8"),
                AlgebraicExpression("3*x1 + s3 = 3"),
            ]
        )
        self.simplex.solve_problem()

    def get_solutions(self):
        return {
            "z": Decimal("0.8"),
            "x1": Decimal("0.8"),
            "s1": Decimal("0"),
            "s2": Decimal("3.2"),
            "s3": Decimal("0.6")
        }

class TestSimplex3_2(TestSimplexBase, unittest.TestCase):

    def setUp(self):
        self.simplex = Simplex(
            num_variables=4,
            objective_function=ObjectiveFunction("z = x1"),
            method=Simplex.MINIMIZE,
            constraints=[
                AlgebraicExpression("5*x1 + s1 = 4"),
                AlgebraicExpression("6*x1 + s2 = 8"),
                AlgebraicExpression("3*x1 + s3 = 3"),
            ]
        )
        self.simplex.solve_problem()

    def get_solutions(self):
        return {
            "z": Decimal("0"),
            "x1": Decimal("0"),
            "s1": Decimal("4"),
            "s2": Decimal("8"),
            "s3": Decimal("3")
        }

class TestSimplex4(TestSimplexBase, unittest.TestCase):

    def setUp(self):
        self.simplex = Simplex(
            num_variables=5,
            objective_function=ObjectiveFunction("z = 5x1 - 6x2 + 3x3 - 5x4 + 12x5"),
            method=Simplex.MAXIMIZE,
            constraints=[
                AlgebraicExpression("x1 + 3x2 + 5x3 + 6x4 + 3x5 <= 90"),
            ]
        )
        self.simplex.solve_problem()

    def get_solutions(self):
        return {
            "z": Decimal("450"),
            "x1": Decimal("90"),
            "x2": Decimal("0"),
            "x3": Decimal("0"),
            "x4": Decimal("0"),
            "x5": Decimal("0")
        }

class TestSimplexDecimal(TestSimplexBase, unittest.TestCase):

    def setUp(self):
        self.simplex = Simplex(
            num_variables=2,
            objective_function=ObjectiveFunction("z = 1.5x1 + 2.5x2"),
            method=Simplex.MAXIMIZE,
            constraints=[
                AlgebraicExpression("0.5x1 + 1.5x2 <= 9"),
                AlgebraicExpression("x1 + x2 <= 6"),
            ]
        )
        self.simplex.solve_problem()

    def get_solutions(self):
        return {
            "z": Decimal("15"),
            "x1": Decimal("0"),
            "x2": Decimal("6"),
        }

class TestErrorSimplex(unittest.TestCase):

    def test_raise_value_error(self):
        simplex = Simplex(
            num_variables=5,
            objective_function=ObjectiveFunction("z = 5x1 - 6x2 + 3x3 - 5x4 + 12x5"),
            method=Simplex.MAXIMIZE,
            constraints=[
                AlgebraicExpression("x1 + 3x2 + 5x3 + 6x4 + 3x5 <= 90"),
                AlgebraicExpression("x1 + 3x2 + 5t3 + 6x4 + 3x5 <= 90"),
            ]
        )
        self.assertRaises(
            ValueError, simplex.solve_problem
        )

if __name__ == '__main__':
    unittest.main()
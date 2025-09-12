import unittest

from functions import ObjectiveFunction

class TestObjectiveFunction(unittest.TestCase):

    def setUp(self):
        self.function_1 = "f(x) = 2x1 + x2 - x3"
        self.function_2 = "y = x1 - 3x2 + 4x3"
        self.function_3 = "z = -2x1 + x2"

    def test_parse_function_1(self):
        f = ObjectiveFunction(self.function_1)
        self.assertEqual(f.coefficients, [2, 1, -1])
        self.assertEqual(f.variables, ['x1', 'x2', 'x3'])
        self.assertEqual(f.function_name, 'f(x)')
        self.assertEqual(f.representation, 'f(x) = 2 * x1 + x2 - x3')

    def test_parse_function_2(self):
        f = ObjectiveFunction(self.function_2)
        self.assertEqual(f.coefficients, [1, -3, 4])
        self.assertEqual(f.variables, ['x1', 'x2', 'x3'])
        self.assertEqual(f.function_name, 'y')
        self.assertEqual(f.representation, 'y = x1 - 3 * x2 + 4 * x3')

    def test_parse_function_3(self):
        f = ObjectiveFunction(self.function_3)
        self.assertEqual(f.coefficients, [-2, 1])
        self.assertEqual(f.variables, ['x1', 'x2'])
        self.assertEqual(f.function_name, 'z')
        self.assertEqual(f.representation, 'z = - 2 * x1 + x2')

    def test_is_a_function(self):
        self.assertTrue(ObjectiveFunction.is_an_objective_function(self.function_1))
        self.assertTrue(ObjectiveFunction.is_an_objective_function(self.function_2))
        self.assertTrue(ObjectiveFunction.is_an_objective_function(self.function_3))

    def test_is_not_a_function(self):
        self.assertFalse(ObjectiveFunction.is_an_objective_function("8 = 2*x1 + x2 - x3"))
        self.assertFalse(ObjectiveFunction.is_an_objective_function("2*x1 + x2 - x3"))
        self.assertFalse(ObjectiveFunction.is_an_objective_function("1 + 1"))
        self.assertFalse(ObjectiveFunction.is_an_objective_function("x = x + x1"))

if __name__ == '__main__':
    unittest.main()
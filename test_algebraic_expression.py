import unittest

from functions import AlgebraicExpression

class TestAlgebraicExpression(unittest.TestCase):

    def setUp(self):
        self.expression_1 = "2*x1 + x2 - x3 = 8"
        self.expression_2 = "x1 - 3 * x2 + 4 * x3 >= -2"
        self.expression_3 = "-2x1 + x2 <= 5"
        self.expression_4 = "-2x1 + x2 > 5"
        self.expression_5 = "-2x1 + x2 < 5"

    def test_parse_expression_1(self):
        exp = AlgebraicExpression(self.expression_1)
        self.assertEqual(exp.coefficients, [2, 1, -1])
        self.assertEqual(exp.variables, ['x1', 'x2', 'x3'])
        self.assertEqual(exp.sign, '=')
        self.assertEqual(exp.independent_term, 8)
        self.assertEqual(exp.representation, "2 * x1 + x2 - x3 = 8")

    def test_parse_expression_2(self):
        exp = AlgebraicExpression(self.expression_2)
        self.assertEqual(exp.coefficients, [1, -3, 4])
        self.assertEqual(exp.variables, ['x1', 'x2', 'x3'])
        self.assertEqual(exp.sign, '>=')
        self.assertEqual(exp.independent_term, -2)
        self.assertEqual(exp.representation, "x1 - 3 * x2 + 4 * x3 >= -2")

    def test_parse_expression_3(self):
        exp = AlgebraicExpression(self.expression_3)
        self.assertEqual(exp.coefficients, [-2, 1])
        self.assertEqual(exp.variables, ['x1', 'x2'])
        self.assertEqual(exp.sign, '<=')
        self.assertEqual(exp.independent_term, 5)
        self.assertEqual(exp.representation, "-2 * x1 + x2 <= 5")

    def test_parse_expression_4(self):
        exp = AlgebraicExpression(self.expression_4)
        self.assertEqual(exp.coefficients, [-2, 1])
        self.assertEqual(exp.variables, ['x1', 'x2'])
        self.assertEqual(exp.sign, '>')
        self.assertEqual(exp.independent_term, 5)
        self.assertEqual(exp.representation, "-2 * x1 + x2 > 5")

    def test_parse_expression_5(self):
        exp = AlgebraicExpression(self.expression_5)
        self.assertEqual(exp.coefficients, [-2, 1])
        self.assertEqual(exp.variables, ['x1', 'x2'])
        self.assertEqual(exp.sign, '<')
        self.assertEqual(exp.independent_term, 5)
        self.assertEqual(exp.representation, "-2 * x1 + x2 < 5")

    def test_zero_expression(self):
        exp = AlgebraicExpression("0x1 + x2 + 0*x3 = 2")
        self.assertEqual(exp.coefficients, [0, 1, 0])
        self.assertEqual(exp.variables, ['x1', 'x2', 'x3'])
        self.assertEqual(exp.sign, '=')
        self.assertEqual(exp.independent_term, 2)
        self.assertEqual(exp.representation, "0 * x1 + x2 + 0 * x3 = 2")

    def test_is_an_algebraic_expression(self):
        self.assertTrue(AlgebraicExpression.is_an_algebraic_expression(self.expression_1))
        self.assertTrue(AlgebraicExpression.is_an_algebraic_expression(self.expression_2))
        self.assertTrue(AlgebraicExpression.is_an_algebraic_expression(self.expression_3))
        self.assertTrue(AlgebraicExpression.is_an_algebraic_expression(self.expression_4))
        self.assertTrue(AlgebraicExpression.is_an_algebraic_expression(self.expression_5))

    def test_is_not_an_algebraic_expression(self):
        self.assertFalse(AlgebraicExpression.is_an_algebraic_expression("1 + 1"))
        self.assertFalse(AlgebraicExpression.is_an_algebraic_expression("x1 + x2"))
        self.assertFalse(AlgebraicExpression.is_an_algebraic_expression("x1 + x2 ="))
        self.assertFalse(AlgebraicExpression.is_an_algebraic_expression("x1 + x2 = x3"))
        self.assertFalse(AlgebraicExpression.is_an_algebraic_expression("x1 + x2 = 1 + x3"))

    # Tests that the method returns 1 for an equation with a single variable
    def test_single_variable(self):
        expression = AlgebraicExpression('2x = 4')
        self.assertEqual(expression.number_of_variables, 1)

    # Tests that the method returns the correct number of variables for an equation with multiple variables
    def test_multiple_variables(self):
        expression = AlgebraicExpression('2x + 3y - 4z = 5')
        self.assertEqual(expression.number_of_variables, 3)

    # Tests that the method returns the correct number of variables for a complex equation with multiple variables and coefficients
    def test_complex_equation(self):
        expression = AlgebraicExpression('2x + 3y - 4z + 5w - 6u = 7')
        self.assertEqual(expression.number_of_variables, 5)

    # Tests that the method returns 0 for an equation with no coefficients
    def test_no_coefficients(self):
        expression = AlgebraicExpression('x + y + z = 5')
        self.assertEqual(expression.number_of_variables, 3)

    def test_repeated_coefficients(self):
        expression = AlgebraicExpression("x1 + x1 + x1 = 2")
        self.assertEqual(expression.number_of_variables, 1)
        self.assertEqual(expression.coefficients, [3,])

if __name__ == '__main__':
    unittest.main()
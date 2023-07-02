import unittest

from funciones import ExpresionAlgebraica

class TestExpresionAlgebraica(unittest.TestCase):

    def setUp(self):
        self.expresion_1 = "2*x1 + x2 - x3 = 8"
        self.expresion_2 = "x1 - 3 * x2 + 4 * x3 >= -2"
        self.expresion_3 = "-2x1 + x2 <= 5"
        self.expresion_4 = "-2x1 + x2 > 5"
        self.expresion_5 = "-2x1 + x2 < 5"

    def test_parse_expresion_1(self):
        exp = ExpresionAlgebraica(self.expresion_1)
        self.assertEqual(exp.coeficientes, [2, 1, -1])
        self.assertEqual(exp.variables, ['x1', 'x2', 'x3'])
        self.assertEqual(exp.signo, '=')
        self.assertEqual(exp.termino_independiente, 8)
        self.assertEqual(exp.representacion, "2 * x1 + x2 - x3 = 8")

    def test_parse_expresion_2(self):
        exp = ExpresionAlgebraica(self.expresion_2)
        self.assertEqual(exp.coeficientes, [1, -3, 4])
        self.assertEqual(exp.variables, ['x1', 'x2', 'x3'])
        self.assertEqual(exp.signo, '>=')
        self.assertEqual(exp.termino_independiente, -2)
        self.assertEqual(exp.representacion, "x1 - 3 * x2 + 4 * x3 >= -2")

    def test_parse_expresion_3(self):
        exp = ExpresionAlgebraica(self.expresion_3)
        self.assertEqual(exp.coeficientes, [-2, 1])
        self.assertEqual(exp.variables, ['x1', 'x2'])
        self.assertEqual(exp.signo, '<=')
        self.assertEqual(exp.termino_independiente, 5)
        self.assertEqual(exp.representacion, "-2 * x1 + x2 <= 5")

    def test_parse_expresion_4(self):
        exp = ExpresionAlgebraica(self.expresion_4)
        self.assertEqual(exp.coeficientes, [-2, 1])
        self.assertEqual(exp.variables, ['x1', 'x2'])
        self.assertEqual(exp.signo, '>')
        self.assertEqual(exp.termino_independiente, 5)
        self.assertEqual(exp.representacion, "-2 * x1 + x2 > 5")

    def test_parse_expresion_5(self):
        exp = ExpresionAlgebraica(self.expresion_5)
        self.assertEqual(exp.coeficientes, [-2, 1])
        self.assertEqual(exp.variables, ['x1', 'x2'])
        self.assertEqual(exp.signo, '<')
        self.assertEqual(exp.termino_independiente, 5)
        self.assertEqual(exp.representacion, "-2 * x1 + x2 < 5")

    def test_zero_expresion(self):
        exp = ExpresionAlgebraica("0x1 + x2 + 0*x3 = 2")
        self.assertEqual(exp.coeficientes, [0, 1, 0])
        self.assertEqual(exp.variables, ['x1', 'x2', 'x3'])
        self.assertEqual(exp.signo, '=')
        self.assertEqual(exp.termino_independiente, 2)
        self.assertEqual(exp.representacion, "0 * x1 + x2 + 0 * x3 = 2")

    def test_es_una_expresion_algebraica(self):
        self.assertTrue(ExpresionAlgebraica.es_una_expresion_algebraica(self.expresion_1))
        self.assertTrue(ExpresionAlgebraica.es_una_expresion_algebraica(self.expresion_2))
        self.assertTrue(ExpresionAlgebraica.es_una_expresion_algebraica(self.expresion_3))
        self.assertTrue(ExpresionAlgebraica.es_una_expresion_algebraica(self.expresion_4))
        self.assertTrue(ExpresionAlgebraica.es_una_expresion_algebraica(self.expresion_5))

    def test_no_es_una_expresion_algebraica(self):
        self.assertFalse(ExpresionAlgebraica.es_una_expresion_algebraica("1 + 1"))
        self.assertFalse(ExpresionAlgebraica.es_una_expresion_algebraica("x1 + x2"))
        self.assertFalse(ExpresionAlgebraica.es_una_expresion_algebraica("x1 + x2 ="))
        self.assertFalse(ExpresionAlgebraica.es_una_expresion_algebraica("x1 + x2 = x3"))
        self.assertFalse(ExpresionAlgebraica.es_una_expresion_algebraica("x1 + x2 = 1 + x3"))

    # Tests that the method returns 1 for an equation with a single variable
    def test_single_variable(self):
        expresion = ExpresionAlgebraica('2x = 4')
        self.assertEqual(expresion.numero_de_variables, 1)

    # Tests that the method returns the correct number of variables for an equation with multiple variables
    def test_multiple_variables(self):
        expresion = ExpresionAlgebraica('2x + 3y - 4z = 5')
        self.assertEqual(expresion.numero_de_variables, 3)

    # Tests that the method returns the correct number of variables for a complex equation with multiple variables and coefficients
    def test_complex_equation(self):
        expresion = ExpresionAlgebraica('2x + 3y - 4z + 5w - 6u = 7')
        self.assertEqual(expresion.numero_de_variables, 5)

    # Tests that the method returns 0 for an equation with no coefficients
    def test_no_coefficients(self):
        expresion = ExpresionAlgebraica('x + y + z = 5')
        self.assertEqual(expresion.numero_de_variables, 3)

    def test_coeficientes_repetidos(self):
        expresion = ExpresionAlgebraica("x1 + x1 + x1 = 2")
        self.assertEqual(expresion.numero_de_variables, 1)
        self.assertEqual(expresion.coeficientes, [3,])

if __name__ == '__main__':
    unittest.main()

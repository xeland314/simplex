import unittest

from expresion import ExpresionAlgebraica

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

    def test_parse_expresion_2(self):
        exp = ExpresionAlgebraica(self.expresion_2)
        self.assertEqual(exp.coeficientes, [1, -3, 4])
        self.assertEqual(exp.variables, ['x1', 'x2', 'x3'])
        self.assertEqual(exp.signo, '>=')
        self.assertEqual(exp.termino_independiente, -2)

    def test_parse_expresion_3(self):
        exp = ExpresionAlgebraica(self.expresion_3)
        self.assertEqual(exp.coeficientes, [-2, 1])
        self.assertEqual(exp.variables, ['x1', 'x2'])
        self.assertEqual(exp.signo, '<=')
        self.assertEqual(exp.termino_independiente, 5)

    def test_parse_expresion_4(self):
        exp = ExpresionAlgebraica(self.expresion_4)
        self.assertEqual(exp.coeficientes, [-2, 1])
        self.assertEqual(exp.variables, ['x1', 'x2'])
        self.assertEqual(exp.signo, '>')
        self.assertEqual(exp.termino_independiente, 5)

    def test_parse_expresion_5(self):
        exp = ExpresionAlgebraica(self.expresion_5)
        self.assertEqual(exp.coeficientes, [-2, 1])
        self.assertEqual(exp.variables, ['x1', 'x2'])
        self.assertEqual(exp.signo, '<')
        self.assertEqual(exp.termino_independiente, 5)

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

if __name__ == '__main__':
    unittest.main()

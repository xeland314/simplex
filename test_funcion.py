import unittest

from funciones import FuncionObjetivo

class TestFuncion(unittest.TestCase):

    def setUp(self):
        self.funcion_1 = "f(x) = 2x1 + x2 - x3"
        self.funcion_2 = "y = x1 - 3x2 + 4x3"
        self.funcion_3 = "z = -2x1 + x2"

    def test_parse_funcion_1(self):
        f = FuncionObjetivo(self.funcion_1)
        self.assertEqual(f.coeficientes, [2, 1, -1])
        self.assertEqual(f.variables, ['x1', 'x2', 'x3'])
        self.assertEqual(f.nombre_funcion, 'f(x)')
        self.assertEqual(f.representacion, 'f(x) = 2 * x1 + x2 - x3')

    def test_parse_funcion_2(self):
        f = FuncionObjetivo(self.funcion_2)
        self.assertEqual(f.coeficientes, [1, -3, 4])
        self.assertEqual(f.variables, ['x1', 'x2', 'x3'])
        self.assertEqual(f.nombre_funcion, 'y')
        self.assertEqual(f.representacion, 'y = x1 - 3 * x2 + 4 * x3')

    def test_parse_funcion_3(self):
        f = FuncionObjetivo(self.funcion_3)
        self.assertEqual(f.coeficientes, [-2, 1])
        self.assertEqual(f.variables, ['x1', 'x2'])
        self.assertEqual(f.nombre_funcion, 'z')
        self.assertEqual(f.representacion, 'z = - 2 * x1 + x2')

    def test_es_una_funcion(self):
        self.assertTrue(FuncionObjetivo.es_una_funcion(self.funcion_1))
        self.assertTrue(FuncionObjetivo.es_una_funcion(self.funcion_2))
        self.assertTrue(FuncionObjetivo.es_una_funcion(self.funcion_3))

    def test_no_es_una_funcion(self):
        self.assertFalse(FuncionObjetivo.es_una_funcion("8 = 2*x1 + x2 - x3"))
        self.assertFalse(FuncionObjetivo.es_una_funcion("2*x1 + x2 - x3"))
        self.assertFalse(FuncionObjetivo.es_una_funcion("1 + 1"))
        self.assertFalse(FuncionObjetivo.es_una_funcion("x = x + x1"))

if __name__ == '__main__':
    unittest.main()

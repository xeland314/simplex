import unittest

from funcion import Funcion

class TestFuncion(unittest.TestCase):

    def setUp(self):
        self.funcion_1 = "f(x) = 2x1 + x2 - x3"
        self.funcion_2 = "y = x1 - 3x2 + 4x3"
        self.funcion_3 = "z = -2x1 + x2"

    def test_parse_funcion_1(self):
        f = Funcion(self.funcion_1)
        self.assertEqual(f.coeficientes, [2, 1, -1])
        self.assertEqual(f.variables, ['x1', 'x2', 'x3'])
        self.assertEqual(f.nombre_funcion, 'f(x)')

    def test_parse_funcion_2(self):
        f = Funcion(self.funcion_2)
        self.assertEqual(f.coeficientes, [1, -3, 4])
        self.assertEqual(f.variables, ['x1', 'x2', 'x3'])
        self.assertEqual(f.nombre_funcion, 'y')

    def test_parse_funcion_3(self):
        f = Funcion(self.funcion_3)
        self.assertEqual(f.coeficientes, [-2, 1])
        self.assertEqual(f.variables, ['x1', 'x2'])
        self.assertEqual(f.nombre_funcion, 'z')

    def test_es_una_funcion(self):
        self.assertTrue(Funcion.es_una_funcion(self.funcion_1))
        self.assertTrue(Funcion.es_una_funcion(self.funcion_2))
        self.assertTrue(Funcion.es_una_funcion(self.funcion_3))

    def test_no_es_una_funcion(self):
        self.assertFalse(Funcion.es_una_funcion("8 = 2*x1 + x2 - x3"))
        self.assertFalse(Funcion.es_una_funcion("2*x1 + x2 - x3"))
        self.assertFalse(Funcion.es_una_funcion("1 + 1"))

if __name__ == '__main__':
    unittest.main()
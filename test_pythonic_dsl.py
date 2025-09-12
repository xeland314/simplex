import unittest
from pythonic_dsl import Model, Var, maximize

class TestPythonicDSL(unittest.TestCase):
    def test_pythonic_dsl(self):
        m = Model("ejemplo_lp")

        x1 = Var("x1", low=0)
        x2 = Var("x2", low=0)

        m += maximize(5 * x1 + 4 * x2)
        m += (6 * x1 + 4 * x2 <= 24)
        m += (x1 + 2 * x2 <= 6)
        m += (-x1 + x2 <= 1)
        m += (x2 <= 2)

        resultado = m.solve()

        self.assertAlmostEqual(resultado.optimal_values[0][1], 21, places=5)
        self.assertAlmostEqual(resultado.optimal_values[1][1], 3, places=5)
        self.assertAlmostEqual(resultado.optimal_values[2][1], 1.5, places=5)

if __name__ == '__main__':
    unittest.main()

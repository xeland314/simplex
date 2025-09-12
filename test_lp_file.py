import unittest
from dsl import DSL
from advanced_simplex import Simplex

class TestLPFile(unittest.TestCase):
    def setUp(self):
        self.dsl = DSL("/home/xeland314/workspace/python/simplex/test.lp")

    def test_create_dsl_and_to_simplex(self):
        self.assertIsNotNone(self.dsl)
        simplex = self.dsl.to_simplex()
        self.assertIsInstance(simplex, Simplex)

    def test_parse_method(self):
        self.assertEqual(self.dsl.method, Simplex.MAXIMIZE)

    def test_parse_objective_function(self):
        self.assertEqual(self.dsl.objective_function.terms['x1'], 5)
        self.assertEqual(self.dsl.objective_function.terms['x2'], 4)

    def test_parse_constraints(self):
        self.assertEqual(len(self.dsl.constraints), 6)
        self.assertEqual(self.dsl.constraints[0].terms['x1'], 6)
        self.assertEqual(self.dsl.constraints[0].terms['x2'], 4)
        self.assertEqual(self.dsl.constraints[0].independent_term, 24)

        self.assertEqual(self.dsl.constraints[1].terms['x1'], 1)
        self.assertEqual(self.dsl.constraints[1].terms['x2'], 2)
        self.assertEqual(self.dsl.constraints[1].independent_term, 6)

        self.assertEqual(self.dsl.constraints[2].terms['x1'], -1)
        self.assertEqual(self.dsl.constraints[2].terms['x2'], 1)
        self.assertEqual(self.dsl.constraints[2].independent_term, 1)

        self.assertEqual(self.dsl.constraints[3].terms['x2'], 1)
        self.assertEqual(self.dsl.constraints[3].independent_term, 2)

        self.assertEqual(self.dsl.constraints[4].terms['x1'], 1)
        self.assertEqual(self.dsl.constraints[4].independent_term, 0)

        self.assertEqual(self.dsl.constraints[5].terms['x2'], 1)
        self.assertEqual(self.dsl.constraints[5].independent_term, 0)

if __name__ == '__main__':
    unittest.main()

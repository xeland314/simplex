import unittest
from dsl import DSL
from advanced_simplex import Simplex

class TestDSL(unittest.TestCase):
    def setUp(self):
        self.problem = """
        MINIMIZE z = 3*x1 + 5*x2
        SUBJECT TO
            2*x1 + x2 >= 8
            x1 + 3*x2 >= 9
            x1 <= 5
            x2 >= 1
        BOUNDS
            x1 >= 0
            x2 free
        """
        self.dsl = DSL(self.problem)

    def test_create_dsl_and_to_simplex(self):
        self.assertIsNotNone(self.dsl)
        simplex = self.dsl.to_simplex()
        self.assertIsInstance(simplex, Simplex)

    def test_parse_method(self):
        self.assertEqual(self.dsl.method, Simplex.MINIMIZE)

    def test_parse_objective_function(self):
        self.assertEqual(self.dsl.objective_function.terms['x1'], 3)
        self.assertEqual(self.dsl.objective_function.terms['x2_plus'], 5)
        self.assertEqual(self.dsl.objective_function.terms['x2_minus'], -5)

    def test_parse_constraints(self):
        self.assertEqual(len(self.dsl.constraints), 7)
        self.assertEqual(self.dsl.constraints[0].terms['x1'], 2)
        self.assertEqual(self.dsl.constraints[0].terms['x2_plus'], 1)
        self.assertEqual(self.dsl.constraints[0].terms['x2_minus'], -1)
        self.assertEqual(self.dsl.constraints[0].independent_term, 8)

        self.assertEqual(self.dsl.constraints[1].terms['x1'], 1)
        self.assertEqual(self.dsl.constraints[1].terms['x2_plus'], 3)
        self.assertEqual(self.dsl.constraints[1].terms['x2_minus'], -3)
        self.assertEqual(self.dsl.constraints[1].independent_term, 9)

        self.assertEqual(self.dsl.constraints[2].terms['x1'], 1)
        self.assertEqual(self.dsl.constraints[2].independent_term, 5)

        self.assertEqual(self.dsl.constraints[3].terms['x2_plus'], 1)
        self.assertEqual(self.dsl.constraints[3].terms['x2_minus'], -1)
        self.assertEqual(self.dsl.constraints[3].independent_term, 1)

        self.assertEqual(self.dsl.constraints[4].terms['x1'], 1)
        self.assertEqual(self.dsl.constraints[4].independent_term, 0)

        self.assertEqual(self.dsl.constraints[5].terms['x2_plus'], 1)
        self.assertEqual(self.dsl.constraints[5].independent_term, 0)
        
        self.assertEqual(self.dsl.constraints[6].terms['x2_minus'], 1)
        self.assertEqual(self.dsl.constraints[6].independent_term, 0)


if __name__ == '__main__':
    unittest.main()
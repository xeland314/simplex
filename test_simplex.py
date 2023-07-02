from abc import ABC, abstractmethod
from decimal import Decimal
import unittest

from advanced_simplex import Simplex
from funciones import ExpresionAlgebraica, FuncionObjetivo

class TestSimplexBase(ABC):

    @abstractmethod
    def setUp(self):
        """
        Se define un problema de optimización con simplex.
        """
        pass


    def test_comprobar_valores_optimos(self):
        """
        Se comprueban las soluciones del sistema.
        """
        soluciones = self.obtener_soluciones()
        for variable, valor in self.simplex.valores_optimos:
            self.assertTrue(soluciones[variable] == valor)

    @abstractmethod
    def obtener_soluciones(self):
        """
        PHPSimplex es una herramienta en línea para resolver problemas
        de programación lineal utilizando el método simplex.
        Su uso es libre y gratuito.
        
        - Link: http://www.phpsimplex.com/simplex/simplex.htm?l=es
        """
        pass

class TestSimplex1(TestSimplexBase, unittest.TestCase):

    def setUp(self):
        self.simplex = Simplex(
            numero_de_variables=6,
            funcion_objetivo=FuncionObjetivo("z = 5x1 + 4x2 + 0s1 + 0s2 + 0s3 + 0s4"),
            metodo=Simplex.MAXIMIZAR,
            restricciones=[
                ExpresionAlgebraica("6x1 + 4x2 + s1 = 24"),
                ExpresionAlgebraica("x1 + 2x2 + s2 = 6"),
                ExpresionAlgebraica("-x1 + x2 + s3 = 1"),
                ExpresionAlgebraica("x2 + s4 = 2")
            ]
        )
        self.simplex.resolver_problema()
        self.simplex.mostrar_resultados()

    def obtener_soluciones(self):
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
            numero_de_variables=4,
            funcion_objetivo=FuncionObjetivo("z = 2x1 + x2 - 3x3 + 5x4"),
            metodo=Simplex.MAXIMIZAR,
            restricciones=[
                ExpresionAlgebraica("x1 + 2x2 + 2x3 + 4x4 <= 40"),
                ExpresionAlgebraica("2x1 - x2 + x3 + 2x4 <= 8"),
                ExpresionAlgebraica("4x1 - 2x2 + x3 - x4 <= 10"),
            ]
        )
        self.simplex.resolver_problema()

    def obtener_soluciones(self):
        return {
            "z": Decimal("41"),
            "x1": Decimal("0"),
            "x2": Decimal("6"),
            "x3": Decimal("0"),
            "x4": Decimal("7")
        }


class TestSimplex2_1(TestSimplex2):

    def obtener_soluciones(self):
        self.simplex.funcion_objetivo = FuncionObjetivo(
            "z = 8x1 + 6x2 + 3x3 - 2x4"
        )
        self.simplex.resolver_problema()
        return {
            "z": Decimal("170"),
            "x1": Decimal("10"),
            "x2": Decimal("15"),
            "x3": Decimal("0"),
            "x4": Decimal("0")
        }

class TestSimplex2_2(TestSimplex2):

    def obtener_soluciones(self):
        self.simplex.funcion_objetivo = FuncionObjetivo(
            "z = 3x1 - x2 + 3x3 + 4x4"
        )
        self.simplex.resolver_problema()
        return {
            "z": Decimal("36"),
            "x1": Decimal("0"),
            "x2": Decimal("6"),
            "x3": Decimal("14"),
            "x4": Decimal("0")
        }

class TestSimplex2_3(TestSimplex2):

    def obtener_soluciones(self):
        self.simplex.funcion_objetivo = FuncionObjetivo(
            "z = 5x1 - 4x2 + 6x3 - 8x4"
        )
        self.simplex.metodo = self.simplex.MINIMIZAR
        self.simplex.resolver_problema()
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
            numero_de_variables=4,
            funcion_objetivo=FuncionObjetivo("z = x1+0*x2+0*x3+0*x4"),
            metodo=Simplex.MAXIMIZAR,
            restricciones=[
                ExpresionAlgebraica("5*x1 + x2 = 4"),
                ExpresionAlgebraica("6*x1 + x3 = 8"),
                ExpresionAlgebraica("3*x1 + x4 = 3"),
            ]
        )
        self.simplex.resolver_problema()

    def obtener_soluciones(self):
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
            numero_de_variables=4,
            funcion_objetivo=FuncionObjetivo("z = x1"),
            metodo=Simplex.MAXIMIZAR,
            restricciones=[
                ExpresionAlgebraica("5*x1 + s1 = 4"),
                ExpresionAlgebraica("6*x1 + s2 = 8"),
                ExpresionAlgebraica("3*x1 + s3 = 3"),
            ]
        )
        self.simplex.resolver_problema()

    def obtener_soluciones(self):
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
            numero_de_variables=4,
            funcion_objetivo=FuncionObjetivo("z = x1"),
            metodo=Simplex.MINIMIZAR,
            restricciones=[
                ExpresionAlgebraica("5*x1 + s1 = 4"),
                ExpresionAlgebraica("6*x1 + s2 = 8"),
                ExpresionAlgebraica("3*x1 + s3 = 3"),
            ]
        )
        self.simplex.resolver_problema()

    def obtener_soluciones(self):
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
            numero_de_variables=5,
            funcion_objetivo=FuncionObjetivo("z = 5x1 - 6x2 + 3x3 - 5x4 + 12x5"),
            metodo=Simplex.MAXIMIZAR,
            restricciones=[
                ExpresionAlgebraica("x1 + 3x2 + 5x3 + 6x4 + 3x5 <= 90"),
            ]
        )
        self.simplex.resolver_problema()

    def obtener_soluciones(self):
        return {
            "z": Decimal("450"),
            "x1": Decimal("90"),
            "x2": Decimal("0"),
            "x3": Decimal("0"),
            "x4": Decimal("0"),
            "x5": Decimal("0")
        }

class TestErrorSimplex(unittest.TestCase):

    def test_raise_value_error(self):
        simplex = Simplex(
            numero_de_variables=5,
            funcion_objetivo=FuncionObjetivo("z = 5x1 - 6x2 + 3x3 - 5x4 + 12x5"),
            metodo=Simplex.MAXIMIZAR,
            restricciones=[
                ExpresionAlgebraica("x1 + 3x2 + 5x3 + 6x4 + 3x5 <= 90"),
                ExpresionAlgebraica("x1 + 3x2 + 5t3 + 6x4 + 3x5 <= 90"),
            ]
        )
        self.assertRaises(
            ValueError, simplex.resolver_problema
        )

if __name__ == '__main__':
    unittest.main()

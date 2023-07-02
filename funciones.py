from abc import ABCMeta, abstractmethod
from collections import Counter
from decimal import Decimal
import re

class ExpresionMatematica(metaclass=ABCMeta):

    def __init__(self, expresion: str) -> None:
        self.expresion = expresion
        self.terminos = Counter()
        self.orden_variables = []
    
    @property
    def coeficientes(self) -> list:
        coeficientes = []
        for variable in self.orden_variables:
            valor = self.terminos.get(variable, 0)
            coeficientes.append(valor)
        return coeficientes

    @property
    def numero_de_variables(self) -> int:
        return len(self.orden_variables)

    @property
    def variables(self) -> list:
        return self.orden_variables

    @abstractmethod
    def _parse_expresion(self) -> None:
        pass

    def __repr__(self) -> str:
        return self.expresion

    def __str__(self) -> str:
        return self.expresion

class FuncionObjetivo(ExpresionMatematica):

    def __init__(self, expresion: str) -> None:
        super().__init__(expresion)
        self._parse_expresion()

    def _parse_expresion(self) -> None:
        """
        Analiza una función dada como una cadena de texto y devuelve
        sus coeficientes, nombres de variables y nombre de la función.

        Args:
            - funcion (str): Una cadena de texto que representa una función.
                - La función debe estar en la forma: "f(x) = ax1 + bx2 + ... + cxn",
                - donde a, b, c, ... son coeficientes.
        """
        # Separar la función en dos partes: lado izquierdo y derecho
        lado_izquierdo, lado_derecho = self.expresion.split('=')

        # Obtener el nombre de la función
        self.nombre_funcion = lado_izquierdo.strip()

        # Obtener los coeficientes y nombres de las variables del lado derecho
        for termino in re.findall(r'([+-]?\s*\d*\s*\*?)\s*(\w+)', lado_derecho):
            coeficiente, variable = termino
            coeficiente: str = coeficiente.replace(' ', '').replace('*', '')
            if coeficiente not in ['', '+', '-']:
                self.terminos[variable] += Decimal(coeficiente)
            else:
                self.terminos[variable] += Decimal((coeficiente if coeficiente else '+') + '1')
            if variable not in self.orden_variables:
                self.orden_variables.append(variable)

    @staticmethod
    def es_una_funcion(funcion: str) -> bool:
        """
        Determina si una cadena de texto dada representa una función algebraica válida.
        
        Args:
            funcion (str): Una cadena de texto que representa una posible función algebraica.
        
        Returns:
            bool: True si la cadena de texto representa una función algebraica válida, False en caso contrario.
        """
        # Verificar que la cadena contenga un signo igual
        # Definir la expresión regular para validar funciones algebraicas
        funcion_regex = r'^\s*[a-zA-Z]+\d?\s*(\(\w+\d?\))?\s*=\s*([+-]?\s*\d*\*?\s*[a-zA-Z]+\d*\s*)+\s*$'
        return bool(re.match(funcion_regex, funcion))


class ExpresionAlgebraica(ExpresionMatematica):
    """
    Clase que representa una ecuación o inecuación.
    
    Esta clase toma una cadena de texto que representa una ecuación o inecuación y
    analiza sus coeficientes, nombres de variables, signo y término independiente.
    """

    def __init__(self, expresion: str) -> None:
        super().__init__(expresion)
        self._parse_expresion()

    def _parse_expresion(self) -> None:
        """
        Analiza una ecuación o inecuación dada como una cadena de texto y encuentra
        sus coeficientes, nombres de variables, signo y término independiente.

        Args:
            - expresion (str): Una cadena de texto que representa una ecuación o inecuación.
                - La ecuación debe estar en la forma: "ax1 + bx2 + ... + cxn = d" o "ax1 + bx2 + ... + cxn <= d",
                - donde a, b, c, ... son coeficientes y
                - d es el término independiente.
                - El signo puede ser "=", "<=", ">=", "<" o ">".
        """
        # Separar la ecuación en dos partes: lado izquierdo y derecho
        lado_izquierdo, lado_derecho = re.split(r'[<>=]=?', self.expresion)

        # Obtener el signo de igualdad o desigualdad
        self.signo: str = re.findall(r'[<>=]=?', self.expresion)[0]

        # Obtener los coeficientes y nombres de las variables del lado izquierdo
        for termino in re.findall(r'([+-]?\s*\d*\s*\*?)\s*(\w+)', lado_izquierdo):
            coeficiente, variable = termino
            coeficiente: str = coeficiente.replace(' ', '').replace('*', '')
            if coeficiente not in ['', '+', '-']:
                self.terminos[variable] += Decimal(coeficiente)
            else:
                self.terminos[variable] += Decimal((coeficiente if coeficiente else '+') + '1')
            if variable not in self.orden_variables:
                self.orden_variables.append(variable)

        # Obtener el término independiente del lado derecho
        self.termino_independiente = Decimal(lado_derecho.strip())

    @staticmethod
    def es_una_expresion_algebraica(expresion: str) -> bool:
        """
        Determina si una cadena de texto dada representa una expresión algebraica válida.

        Args:
            - expresion(str): Una cadena de texto que representa una posible expresión algebraica.

        Returns:
            - bool: True si la cadena de texto representa una expresión algebraica válida,
            False en caso contrario.
        """
        patron = r'^\s*[+-]?\s*\d*\s*\*?\s*\w+\s*([+-]\s*\d*\s*\*?\s*\w+\s*)*([<>=]=?)\s*[+-]?\d+\s*$'
        return bool(re.match(patron, expresion))

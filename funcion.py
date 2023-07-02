from decimal import Decimal
import re

class Funcion:
    """
    Clase que representa una función.
    """

    def __init__(self, funcion: str) -> None:
        self.funcion = funcion
        self.parse_funcion(funcion)

    @property
    def numero_de_variables(self) -> int:
        return len(self.coeficientes)

    def parse_funcion(self, funcion: str) -> None:
        """
        Analiza una función dada como una cadena de texto y devuelve
        sus coeficientes, nombres de variables y nombre de la función.

        Args:
            - funcion (str): Una cadena de texto que representa una función.
                - La función debe estar en la forma: "f(x) = ax1 + bx2 + ... + cxn",
                - donde a, b, c, ... son coeficientes.
        """
        # Separar la función en dos partes: lado izquierdo y derecho
        lado_izquierdo, lado_derecho = funcion.split('=')

        # Obtener el nombre de la función
        self.nombre_funcion = lado_izquierdo.strip()

        # Obtener los coeficientes y nombres de las variables del lado derecho
        self.coeficientes, self.variables = [], []
        for termino in re.findall(r'([+-]?\s*\d*\s*\*?)\s*(\w+)', lado_derecho):
            coeficiente, variable = termino
            coeficiente: str = coeficiente.replace(' ', '').replace('*', '')
            if coeficiente not in ['', '+', '-']:
                self.coeficientes.append(Decimal(coeficiente))
            else:
                self.coeficientes.append(Decimal((coeficiente if coeficiente else '+') + '1'))
            self.variables.append(variable)

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

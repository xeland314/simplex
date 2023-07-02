from collections import OrderedDict
import re

class Funcion:
    """
    Clase que representa una función.
    """

    def __init__(self, funcion: str) -> None:
        self.funcion = funcion
        self.terminos = OrderedDict()
        self.parse_funcion(funcion)

    @property
    def coeficientes(self) -> list:
        return list(self.terminos.values())

    @property
    def variables(self) -> list:
        return list(self.terminos.keys())

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
        for termino in re.findall(r'([+-]?\s*\d*\s*\*?)\s*(\w+)', lado_derecho):
            coeficiente, variable = termino
            coeficiente: str = coeficiente.replace(' ', '').replace('*', '')
            if coeficiente not in ['', '+', '-']:
                self.terminos[variable] = (int(coeficiente))
            else:
                self.terminos[variable] = (int((coeficiente if coeficiente else '+') + '1'))

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

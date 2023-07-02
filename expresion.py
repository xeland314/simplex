from collections import OrderedDict
import re

class ExpresionAlgebraica:
    """
    Clase que representa una ecuación o inecuación.
    
    Esta clase toma una cadena de texto que representa una ecuación o inecuación y
    analiza sus coeficientes, nombres de variables, signo y término independiente.
    """

    def __init__(self, expresion: str) -> None:
        self.expresion = expresion
        self.terminos = OrderedDict()
        self.parse_expresion(expresion)

    @property
    def coeficientes(self) -> list:
        return list(self.terminos.values())

    @property
    def variables(self) -> list:
        return list(self.terminos.keys())

    def parse_expresion(self, expresion: str) -> None:
        """
        Analiza una ecuación o inecuación dada como una cadena de texto y devuelve
        sus coeficientes, nombres de variables, signo y término independiente.

        Args:
            - expresion (str): Una cadena de texto que representa una ecuación o inecuación.
                - La ecuación debe estar en la forma: "ax1 + bx2 + ... + cxn = d" o "ax1 + bx2 + ... + cxn <= d",
                - donde a, b, c, ... son coeficientes y
                - d es el término independiente.
                - El signo puede ser "=", "<=", ">=", "<" o ">".
        """
        # Separar la ecuación en dos partes: lado izquierdo y derecho
        lado_izquierdo, lado_derecho = re.split(r'[<>=]=?', expresion)

        # Obtener el signo de igualdad o desigualdad
        self.signo: str = re.findall(r'[<>=]=?', expresion)[0]

        # Obtener los coeficientes y nombres de las variables del lado izquierdo
        for termino in re.findall(r'([+-]?\s*\d*\s*\*?)\s*(\w+)', lado_izquierdo):
            coeficiente, variable = termino
            coeficiente: str = coeficiente.replace(' ', '').replace('*', '')
            if coeficiente not in ['', '+', '-']:
                self.terminos[variable] = int(coeficiente)
            else:
                self.terminos[variable] = int((coeficiente if coeficiente else '+') + '1')

        # Obtener el término independiente del lado derecho
        self.termino_independiente = int(lado_derecho.strip())

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
        try:
            ExpresionAlgebraica(expresion)
            return True
        except:
            return False

from decimal import Decimal
import re

class ExpresionAlgebraica:
    """
    Clase que representa una ecuación o inecuación.
    
    Esta clase toma una cadena de texto que representa una ecuación o inecuación y
    analiza sus coeficientes, nombres de variables, signo y término independiente.
    """

    def __init__(self, expresion: str) -> None:
        self.expresion = expresion
        self.parse_expresion(expresion)

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
        self.coeficientes, self.variables = [], []
        for termino in re.findall(r'([+-]?\s*\d*\s*\*?)\s*(\w+)', lado_izquierdo):
            coeficiente, variable = termino
            coeficiente: str = coeficiente.replace(' ', '').replace('*', '')
            if coeficiente not in ['', '+', '-']:
                self.coeficientes.append(Decimal(coeficiente))
            else:
                self.coeficientes.append(Decimal((coeficiente if coeficiente else '+') + '1'))
            self.variables.append(variable)

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

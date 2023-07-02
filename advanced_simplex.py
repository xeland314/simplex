from decimal import Decimal, ROUND_HALF_UP
import os

from rich.console import Console
from rich.table import Table
from scipy.optimize import linprog

from expresion import ExpresionAlgebraica
from funcion import Funcion

limpiar_terminal = lambda: os.system('cls' if os.name == 'nt' else 'clear')

class Simplex:

    MINIMIZAR = 0
    MAXIMIZAR = 1
    PRECISION = Decimal('0.000001')

    def __call__(self):
        self.__ingresar_numero_de_variables()
        self.__ingresar_funcion_objetivo()
        self.__seleccionar_metodo()
        self.__ingresar_numero_de_restricciones()
        self.__ingresar_restricciones()
        self.__preparar_datos()
        self.__resolver_problema()
        self.mostrar_resultados()

    def __ingresar_numero_de_variables(self) -> None:
        self.numero_de_variables = 0
        while(self.numero_de_variables <= 0):
            limpiar_terminal()
            try:
                self.numero_de_variables = int(
                    input("Ingrese el número de variables: ")
                )
            except Exception:
                pass

    def __ingresar_funcion_objetivo(self) -> None:
        entrada: str = ""
        while(not Funcion.es_una_funcion(entrada)):
            limpiar_terminal()
            print("Formato de la función: z = ax1 + bx2 + ... + cxn")
            print("a, b, c son números.")
            entrada = input("Ingrese la función objetivo: ")
        self.funcion_objetivo = Funcion(entrada)
        self.c = self.funcion_objetivo.coeficientes

    def __seleccionar_metodo(self) -> None:
        self.metodo = -1
        while(not(self.metodo == self.MAXIMIZAR or self.metodo == self.MINIMIZAR)):
            limpiar_terminal()
            try:
                self.metodo = int(
                    input("Desea maximizar (1) o minimizar (0) la función objetivo?: ")
                )
            except Exception:
                pass
        if self.metodo == self.MAXIMIZAR:
            self.c = [-ci for ci in self.c]

    def __ingresar_numero_de_restricciones(self) -> None:
        self.numero_de_reestricciones = 0
        while(self.numero_de_reestricciones <= 0):
            limpiar_terminal()
            try:
                self.numero_de_reestricciones = int(
                    input("Ingrese el número de restricciones: ")
                )
            except Exception:
                pass

    def __ingresar_restricciones(self) -> None:
        self.restricciones: list[ExpresionAlgebraica] = []
        for r in range(self.numero_de_reestricciones):
            entrada: str = ""
            while(not ExpresionAlgebraica.es_una_expresion_algebraica(entrada)):
                limpiar_terminal()
                print("Formato de la restricción: ax1 + bx2 + ... + cxn = d")
                print("a, b, c, d son números.")
                entrada = input(f"Ingrese la restricción #{r + 1}: ")
            self.restricciones.append(
                ExpresionAlgebraica(entrada)
            )
        limpiar_terminal()

    def __preparar_datos(self) -> None:
        self.A, self.b = [], []
        for restriccion in self.restricciones:
            fila = restriccion.coeficientes
            signo = restriccion.signo
            if signo == '<=':
                # la restricción es del tipo Ax <= b
                self.A.append(fila)
                self.b.append(restriccion.termino_independiente)
            elif signo == '>=':
                # la restricción es del tipo Ax >= b,
                # se multiplica todo por -1
                self.A.append([-aij for aij in fila])
                self.b.append(-restriccion.termino_independiente)
            elif signo == '<':
                # la restricción es del tipo Ax < b,
                # se resta un pequeño valor a b
                # para convertirla en Ax <= b - epsilon
                self.A.append(fila)
                self.b.append(restriccion.termino_independiente - Decimal("1e-6"))
            elif signo == '>':
                # la restricción es del tipo Ax > b,
                # se multiplica todo por -1
                # y se resta un pequeño valor a b
                # para convertirla en -Ax <= -b + epsilon
                self.A.append([-aij for aij in fila])
                self.b.append(-restriccion.termino_independiente + Decimal("1e-6"))
            elif signo == '=':
                # la restricción es del tipo Ax = b
                self.A.append(fila)
                self.b.append(restriccion.termino_independiente)
                # agregar restricción de tipo -Ax <= -b
                self.A.append([-aij for aij in fila])
                self.b.append(-self.b[-1])

    def __resolver_problema(self) -> None:
        # Definir los límites de las variables
        self.bounds = [(0, None) for _ in range(self.numero_de_variables)]

        # Resolver el problema de programación lineal
        self.respuesta = linprog(
            self.c, A_ub=self.A, b_ub=self.b,
            bounds=self.bounds, method='highs'
        )

    def mostrar_resultados(self) -> None:
        limpiar_terminal()
        if not self.respuesta.success:
            print('No se pudo encontrar una solución óptima.')
            return
        # Imprimir resultado si se encontró una solución óptima
        table = Table(title="Resultados", title_justify="center")
        table.add_column(header="Variables", justify="center", style="magenta")
        table.add_column(header="Valores óptimos", justify="left", style="green")
        valor = -self.respuesta.fun if self.metodo == self.MAXIMIZAR else self.respuesta.fun
        valor = Decimal(valor)
        valor = valor.quantize(self.PRECISION, ROUND_HALF_UP)
        table.add_row(self.funcion_objetivo.nombre_funcion, str(valor))
        for variable, valor in zip(self.funcion_objetivo.variables, self.respuesta.x):
            valor = Decimal(valor)
            valor = valor.quantize(self.PRECISION, ROUND_HALF_UP)
            table.add_row(variable, str(valor))
        console = Console()
        console.print(table)

if __name__ == "__main__":
    ejecutar_simplex = Simplex()
    ejecutar_simplex()

from decimal import Decimal, ROUND_HALF_UP
import os

from rich.console import Console
from rich.table import Table
from scipy.optimize import linprog

from funciones import ExpresionAlgebraica, FuncionObjetivo

limpiar_terminal = lambda: os.system('cls' if os.name == 'nt' else 'clear')

class Simplex:

    MINIMIZAR = 0
    MAXIMIZAR = 1
    PRECISION = Decimal('0.000001')
    VARIABLE_POR_DEFECTO = "s"

    def __init__(self,
        numero_de_variables = 0,
        funcion_objetivo: FuncionObjetivo = None,
        metodo = -1,
        numero_de_reestricciones = 0,
        restricciones: list[ExpresionAlgebraica] = []
    ):
        self.numero_de_variables = numero_de_variables
        self.funcion_objetivo = funcion_objetivo
        self.metodo = metodo
        self.numero_de_reestricciones = numero_de_reestricciones
        self.restricciones = restricciones
        self.A, self.b, self.c = [], [], []

    def __call__(self):
        self.__ingresar_numero_de_variables()
        self.__ingresar_funcion_objetivo()
        self.__seleccionar_metodo()
        self.__ingresar_numero_de_restricciones()
        self.__ingresar_restricciones()
        self.resolver_problema()
        self.mostrar_resultados()

    def __ingresar_numero_de_variables(self) -> None:
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
        while(not FuncionObjetivo.es_una_funcion(entrada)):
            limpiar_terminal()
            print("Formato de la función: z = ax1 + bx2 + ... + cxn")
            print("a, b, c son números.")
            entrada = input("Ingrese la función objetivo: ")
        self.funcion_objetivo = FuncionObjetivo(entrada)

    def __completar_funcion_objetivo(self) -> None:
        if self.funcion_objetivo.numero_de_variables != self.numero_de_variables:
            variables_faltantes = self.numero_de_variables - self.funcion_objetivo.numero_de_variables
            for valor in range(variables_faltantes):
                self.funcion_objetivo.orden_variables.append(
                    f"{self.VARIABLE_POR_DEFECTO}{valor + 1}"
                )

    def __seleccionar_metodo(self) -> None:
        while(not(self.metodo == self.MAXIMIZAR or self.metodo == self.MINIMIZAR)):
            limpiar_terminal()
            try:
                self.metodo = int(
                    input("Desea maximizar (1) o minimizar (0) la función objetivo?: ")
                )
            except Exception:
                pass

    def __ingresar_numero_de_restricciones(self) -> None:
        while(self.numero_de_reestricciones <= 0):
            limpiar_terminal()
            try:
                self.numero_de_reestricciones = int(
                    input("Ingrese el número de restricciones: ")
                )
            except Exception:
                pass

    def __ingresar_restricciones(self) -> None:
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

    def __completar_restricciones(self) -> None:
        for restriccion in self.restricciones:
            if restriccion.variables == self.funcion_objetivo.variables:
                continue
            restriccion.orden_variables = self.funcion_objetivo.variables

    def __verificar_restricciones(self) -> None:
        variables_f = set(self.funcion_objetivo.variables)
        for restriccion in self.restricciones:
            variables_r = set(restriccion.variables)
            if not variables_r.issubset(variables_f):
                variables = variables_r.difference(variables_f)
                raise ValueError(
                    f"Las variable{'s' if len(variables) > 1 else ''} {variables} "
                    f"de la restriccion {restriccion} "
                    f"no existe{'n' if len(variables) > 1 else ''} "
                    f"en la función objetivo: {self.funcion_objetivo}.\n"
                    "No se puede continuar con la ejecución del programa."
                )

    def __preparar_datos(self) -> None:
        self.__completar_funcion_objetivo()
        self.__verificar_restricciones()
        self.__completar_restricciones()
        self.c = self.funcion_objetivo.coeficientes
        self.c = [-ci for ci in self.c]
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

    def resolver_problema(self) -> None:
        self.__preparar_datos()
        # Definir los límites de las variables
        self.bounds = [(0, None) for _ in range(self.numero_de_variables)]

        # Resolver el problema de programación lineal
        self.respuesta = linprog(
            self.c, A_ub=self.A, b_ub=self.b,
            bounds=self.bounds, method='highs'
        )

        #Guardar valores óptimos
        self.valores_optimos = []
        valor = -self.respuesta.fun
        valor = Decimal(valor).quantize(self.PRECISION, ROUND_HALF_UP)
        self.valores_optimos.append((self.funcion_objetivo.nombre_funcion, valor.normalize()))
        for variable, valor in zip(self.funcion_objetivo.variables, self.respuesta.x):
            valor = Decimal(valor).quantize(self.PRECISION, ROUND_HALF_UP)
            self.valores_optimos.append((variable, valor.normalize()))

    def mostrar_resultados(self) -> None:
        limpiar_terminal()
        if not self.respuesta.success:
            print('No se pudo encontrar una solución óptima.')
            return
        # Imprimir resultado si se encontró una solución óptima
        table = Table(title="Resultados", title_justify="center")
        table.add_column(header="Variables", justify="center", style="magenta")
        table.add_column(header="Valores óptimos", justify="left", style="green")
        for variable, valor in self.valores_optimos:
            table.add_row(variable, str(valor))
        console = Console()
        console.print(table)

if __name__ == "__main__":
    ejecutar_simplex = Simplex()
    ejecutar_simplex()

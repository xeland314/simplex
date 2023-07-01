from decimal import Decimal
import heapq

class AlgoritmoSimplex:
    
    def __init__(self, matriz, b, c):
        self.matriz = matriz
        self.b = b
        self.c = c
        self.tabla = self.crear_tabla_inicial(c, matriz, b)

    def transformar_fila_a_columna(self, i):
        return [fila[i] for fila in self.matriz]

    def transponer(self):
        return [
            self.transformar_fila_a_columna(i) for i in range(len(self.matriz[0]))
        ]

    def es_una_columna_de_pivote(self, columna):
        return (len([c for c in columna if c == 0]) == len(columna) - 1) and sum(columna) == 1

    def valor_variable_para_columna_pivote(self, tabla, columna):
        fila_pivote = [i for (i, x) in enumerate(columna) if x == 1][0]
        return tabla[fila_pivote][-1]

    def crear_tabla_inicial(self, c, matriz, b):
        tabla = [fila[:] + [x] for fila, x in zip(matriz, b)]
        tabla.append([ci for ci in c] + [0])
        return tabla

    def calcular_solucion_primaria(self):
        columnas = self.transponer(self.tabla)
        indices = [
            j for j, columna in enumerate(columnas[:-1]) if self.es_una_columna_de_pivote(columna)
        ]
        return [(
            indice_columna,
            self.valor_variable_para_columna_pivote(self.tabla, columnas[indice_columna])
            ) for indice_columna in indices
        ]

    def calcular_valor_objetivo(self):
        return -(self.tabla[-1][-1])

    def se_puede_mejorar_la_solucion(self):
        fila_funcion_objetivo = self.tabla[-1]
        return any(x > 0 for x in fila_funcion_objetivo[:-1])

    def hay_mas_de_un_minimo(self, L):
        if len(L) <= 1:
            return False

        x,y = heapq.nsmallest(2, L, key=lambda x: x[1])
        return x == y

    def buscar_indice_de_pivote(self):
        # pick minimum positive index of the last row
        columnas = [(i,x) for (i,x) in enumerate(self.tabla[-1][:-1]) if x > 0]
        columna = min(columnas, key=lambda a: a[1])[0]

        # check if unbounded
        if all(fila[columna] <= 0 for fila in self.tabla):
            raise Exception('Linear program is unbounded.')

        # check for degeneracy: more than one minimizer of the quotient
        cocientes = [(i, r[-1] / r[columna])
            for i, r in enumerate(self.tabla[:-1]) if r[columna] > 0]

        if self.hay_mas_de_un_minimo(cocientes):
            raise Exception('Linear program is degenerate.')

        # pick row index minimizing the quotient
        fila = min(cocientes, key=lambda x: x[1])[0]

        return fila, columna

    def realizar_operacion_pivote(self, tabla, pivote):
        i, j = pivote
        valor_pivote = tabla[i][j]
        tabla[i] = [x / valor_pivote for x in tabla[i]]
        for k, _ in enumerate(tabla):
            if k != i:
                multiplo_fila_pivote = [y * tabla[k][j] for y in tabla[i]]
                tabla[k] = [x - y for x,y in zip(tabla[k], multiplo_fila_pivote)]

    def simplex_para_maximizar(self, c, A, b):
        '''
        simplex: [float], [[float]], [float] -> [float], float
        Solve the given standard-form linear program:

            max <c,x>
            s.t. Ax = b
                x >= 0

        providing the optimal solution x* and the value of the objective function
        '''
        print("Initial tableau:")
        for fila in self.tabla:
            print(fila)
        print()

        while self.se_puede_mejorar_la_solucion(self.tabla):
            pivote = self.buscar_indice_de_pivote(self.tabla)
            print("Next pivot index is=%d,%d \n" % pivote)
            self.realizar_operacion_pivote(self.tabla, pivote)
            print("Tableau after pivot:")
            for fila in self.tabla:
                print(fila)
            print()

        return (
            self.tabla,
            self.calcular_solucion_primaria(self.tabla),
            self.calcular_valor_objetivo(self.tabla)
        )

    def simplex_para_minimizar(self):
        '''
        simplex_min: [float], [[float]], [float] -> [float], float
        Solve the given standard-form linear program:

            min <c,x>
            s.t. Ax = b
                    x >= 0

        providing the optimal solution x* and the value of the objective function
        '''
        # Transform the minimization problem into a maximization problem by
        # changing the sign of the objective function coefficients
        c_max = [-ci for ci in self.c]
        
        # Solve the maximization problem using the simplex function
        tableau, primal_solution, max_value = self.simplex_para_maximizar(c_max, self.matriz, self.b)
        
        # Change the sign of the optimal value to obtain the optimal value of the
        # minimization problem
        min_value = -max_value
        
        return tableau, primal_solution, min_value

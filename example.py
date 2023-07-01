import heapq

def transformar_fila_a_columna(matriz, j):
   return [row[j] for row in matriz]

def transponer(matriz):
   return [transformar_fila_a_columna(matriz, j) for j in range(len(matriz[0]))]

def es_una_columna_de_pivote(columna):
   return (len([c for c in columna if c == 0]) == len(columna) - 1) and sum(columna) == 1

def valor_variable_para_columna_pivote(tabla, columna):
   fila_pivote = [i for (i, x) in enumerate(columna) if x == 1][0]
   return tabla[fila_pivote][-1]

# assume the last m columns of A are the slack variables; the initial basis is
# the set of slack variables
def crear_tabla_inicial(c, A, b):
   tabla = [fila[:] + [x] for fila, x in zip(A, b)]
   tabla.append([ci for ci in c] + [0])
   return tabla

def calcular_solucion_primaria(tabla):
   # the pivot columns denote which variables are used
   columnas = transponer(tabla)
   indices = [j for j, columna in enumerate(columnas[:-1]) if es_una_columna_de_pivote(columna)]
   return [(
      indice_columna, valor_variable_para_columna_pivote(tabla, columnas[indice_columna])
      ) for indice_columna in indices
   ]

def calcular_valor_objetivo(tabla):
   return -(tabla[-1][-1])

def se_puede_mejorar_la_solucion(tabla):
   fila_funcion_objetivo = tabla[-1]
   return any(x > 0 for x in fila_funcion_objetivo[:-1])

# this can be slightly faster
def hay_mas_de_un_minimo(L):
   if len(L) <= 1:
      return False

   x,y = heapq.nsmallest(2, L, key=lambda x: x[1])
   return x == y

def buscar_indice_de_pivote(tabla):
   # pick minimum positive index of the last row
   columnas = [(i,x) for (i,x) in enumerate(tabla[-1][:-1]) if x > 0]
   columna = min(columnas, key=lambda a: a[1])[0]

   # check if unbounded
   if all(fila[columna] <= 0 for fila in tabla):
      raise Exception('Linear program is unbounded.')

   # check for degeneracy: more than one minimizer of the quotient
   cocientes = [(i, r[-1] / r[columna])
      for i, r in enumerate(tabla[:-1]) if r[columna] > 0]

   if hay_mas_de_un_minimo(cocientes):
      raise Exception('Linear program is degenerate.')

   # pick row index minimizing the quotient
   fila = min(cocientes, key=lambda x: x[1])[0]

   return fila, columna

def realizar_operacion_pivote(tabla, pivote):
   i, j = pivote
   valor_pivote = tabla[i][j]
   tabla[i] = [x / valor_pivote for x in tabla[i]]
   for k, _ in enumerate(tabla):
      if k != i:
         multiplo_fila_pivote = [y * tabla[k][j] for y in tabla[i]]
         tabla[k] = [x - y for x,y in zip(tabla[k], multiplo_fila_pivote)]

def simplex_para_maximizar(c, A, b):
   '''
   simplex: [float], [[float]], [float] -> [float], float
   Solve the given standard-form linear program:

      max <c,x>
      s.t. Ax = b
           x >= 0

   providing the optimal solution x* and the value of the objective function
   '''
   tabla = crear_tabla_inicial(c, A, b)
   print("Initial tableau:")
   for fila in tabla:
      print(fila)
   print()

   while se_puede_mejorar_la_solucion(tabla):
      pivote = buscar_indice_de_pivote(tabla)
      print("Next pivot index is=%d,%d \n" % pivote)
      realizar_operacion_pivote(tabla, pivote)
      print("Tableau after pivot:")
      for fila in tabla:
         print(fila)
      print()

   return tabla, calcular_solucion_primaria(tabla), calcular_valor_objetivo(tabla)

def simplex_para_minimizar(c, A, b):
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
   c_max = [-ci for ci in c]
   
   # Solve the maximization problem using the simplex function
   tableau, primal_solution, max_value = simplex_para_maximizar(c_max, A, b)
   
   # Change the sign of the optimal value to obtain the optimal value of the
   # minimization problem
   min_value = -max_value
   
   return tableau, primal_solution, min_value

if __name__ == "__main__":
   c = [300, 250, 450]
   A = [[15, 20, 25], [35, 60, 60], [20, 30, 25], [0, 250, 0]]
   b = [1200, 3000, 1500, 500]

   # add slack variables by hand
   A[0] += [1,0,0,0]
   A[1] += [0,1,0,0]
   A[2] += [0,0,1,0]
   A[3] += [0,0,0,1]
   c += [0,0,0,0]

   t, s, v = simplex_para_maximizar(c, A, b)
   print(t)
   print(s)
   print(v)

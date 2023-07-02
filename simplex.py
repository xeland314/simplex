from scipy.optimize import linprog

def simplex():
    # Pedir el número de variables
    n_vars = int(input('Ingrese el número de variables: '))

    # Pedir la función objetivo
    c = [0] * n_vars
    print('Ingrese los coeficientes de la función objetivo:')
    for i in range(n_vars):
        c[i] = float(input(f'x{i+1}: '))

    # Elegir si se va a maximizar o minimizar
    max_min = int(input('¿Desea maximizar (1) o minimizar (0) la función objetivo?: '))

    # Invertir el sentido de la función objetivo si se va a minimizar
    if max_min == 1:
        c = [-ci for ci in c]

    # Pedir el número de n_constr
    n_constr = int(input('Ingrese el número de restricciones: '))

    # Pedir las n_constr y su desigualdad
    A = []
    b = []
    print('Ingrese las restricciones:')
    for i in range(n_constr):
        print(f'Restricción {i+1}:')
        row = [float(input(f'x{j+1}: ')) for j in range(n_vars)]
        inequality = input('Desigualdad (<=, >=, <, > o =): ')
        if inequality == '<=':
            # la restricción es del tipo Ax <= b
            A.append(row)
            b.append(float(input('b: ')))
        elif inequality == '>=':
            # la restricción es del tipo Ax >= b,
            # se multiplica todo por -1
            A.append([-aij for aij in row])
            b.append(-float(input('b: ')))
        elif inequality == '<':
            # la restricción es del tipo Ax < b,
            # se resta un pequeño valor a b
            # para convertirla en Ax <= b - epsilon
            A.append(row)
            b.append(float(input('b: ')) - 1e-6)
        elif inequality == '>':
            # la restricción es del tipo Ax > b,
            # se multiplica todo por -1
            # y se resta un pequeño valor a b
            # para convertirla en -Ax <= -b + epsilon
            A.append([-aij for aij in row])
            b.append(-float(input('b: ')) + 1e-6)
        elif inequality == '=':
            # la restricción es del tipo Ax = b
            A.append(row)
            b.append(float(input('b: ')))
            # agregar restricción de tipo -Ax <= -b
            A.append([-aij for aij in row])
            b.append(-b[-1])
    
    # Definir los límites de las variables
    bounds = [(0, None) for _ in range(n_vars)]

    # Resolver el problema de programación lineal
    respuesta = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

    # Imprimir resultado si se encontró una solución óptima
    if respuesta.success:
        print(f'Óptimo de la función objetivo: {-respuesta.fun if max_min == 1 else respuesta.fun}')
        print(f'Óptimos de las variables: {respuesta.x}')
    else:
        print('No se pudo encontrar una solución óptima.')

    print(respuesta)

if __name__ == '__main__':
    simplex()

from scipy.optimize import linprog

def simplex():
    # Ask for the number of variables
    n_vars = int(input('Enter the number of variables: '))

    # Ask for the objective function
    c = [0] * n_vars
    print('Enter the coefficients of the objective function:')
    for i in range(n_vars):
        c[i] = float(input(f'x{i+1}: '))

    # Choose whether to maximize or minimize
    max_min = int(input('Do you want to maximize (1) or minimize (0) the objective function?: '))

    # Invert the sense of the objective function if it is to be minimized
    if max_min == 1:
        c = [-ci for ci in c]

    # Ask for the number of constraints
    n_constr = int(input('Enter the number of constraints: '))

    # Ask for the constraints and their inequality
    A = []
    b = []
    print('Enter the constraints:')
    for i in range(n_constr):
        print(f'Constraint {i+1}:')
        row = [float(input(f'x{j+1}: ')) for j in range(n_vars)]
        inequality = input('Inequality (<=, >=, <, > or =): ')
        if inequality == '<=':
            # the constraint is of the type Ax <= b
            A.append(row)
            b.append(float(input('b: ')))
        elif inequality == '>=':
            # the constraint is of the type Ax >= b,
            # everything is multiplied by -1
            A.append([-aij for aij in row])
            b.append(-float(input('b: ')))
        elif inequality == '<':
            # the constraint is of the type Ax < b,
            # a small value is subtracted from b
            # to convert it to Ax <= b - epsilon
            A.append(row)
            b.append(float(input('b: ')) - 1e-6)
        elif inequality == '>':
            # the constraint is of the type Ax > b,
            # everything is multiplied by -1
            # and a small value is subtracted from b
            # to convert it to -Ax <= -b + epsilon
            A.append([-aij for aij in row])
            b.append(-float(input('b: ')) + 1e-6)
        elif inequality == '=':
            # the constraint is of the type Ax = b
            A.append(row)
            b.append(float(input('b: ')))
            # add constraint of type -Ax <= -b
            A.append([-aij for aij in row])
            b.append(-b[-1])

    # Define the bounds of the variables
    bounds = [(0, None) for _ in range(n_vars)]

    # Solve the linear programming problem
    response = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

    # Print result if an optimal solution was found
    if response.success:
        print(f'Optimum of the objective function: {-response.fun if max_min == 1 else response.fun}')
        print(f'Optimal variables: {response.x}')
    else:
        print('Could not find an optimal solution.')

    print(response)

if __name__ == '__main__':
    simplex()
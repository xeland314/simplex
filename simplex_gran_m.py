from typing import Optional
import numpy as np
from decimal import Decimal
from scipy import optimize as op

class Simplex:
    def __init__(self,
        A: list = [],
        b: list = [],
        c: list = [],
        tipo: Optional[float|Decimal] = float
    ):
        self._A = np.array(A, dtype=tipo)
        self._b = np.array(b, dtype=tipo)
        self._c = np.array(c, dtype=tipo)
        self.row = len(self._b)
        self.var = len(self._c)

    def solve(self):
        self._A = np.array([[1, -1, 1]], dtype=Decimal)
        self._b = np.array([2], dtype=Decimal)
        self._c = np.array([2, 1, 1], dtype=Decimal)
        self.row = len(self._b)
        self.var = len(self._c)
        (x, obj) = self.simplex(self._A, self._b, self._c)
        self.pprint(x, obj, [])

    def pprint(self, x, obj, A):
        px = ['x_%d = %f' % (i + 1, x[i]) for i in range(len(x))]
        print(','.join(px))
        print('Función de objetivo mínimo: %f' % obj)
        for i in range(len(A)):
            print('%d-th line constraint value is : %f' % (i + 1, x.dot(A[i])))

    def inicializar_simplex(self, A, b):
        b_min, min_pos = (np.min(b), np.argmin(b))
        if b_min < 0:
            for i in range(self.row):
                if i != min_pos:
                    A[i] = A[i] - A[min_pos]
                    b[i] = b[i] - b[min_pos]
            A[min_pos] = A[min_pos] * -1
            b[min_pos] = b[min_pos] * -1
        slacks = np.eye(self.row)
        A = np.concatenate((A, slacks), axis=1)
        c = np.concatenate((np.zeros(self.var), np.ones(self.row)), axis=0)
        new_B = [i + self.var for i in range(self.row)]
        obj = np.sum(b)
        c = c[new_B].reshape(1, -1).dot(A) - c
        c = c[0]
        e = np.argmax(c)
        while c[e] > 0:
            theta = []
            for i in range(len(b)):
                if A[i][e] > 0:
                    theta.append(b[i] / A[i][e])
                else:
                    theta.append(Decimal("inf"))
            l = np.argmin(np.array(theta))
            if theta[l] == Decimal('inf'):
                print('unbounded')
                return False
            (new_B, A, b, c, obj) = self.hallar_pivote(new_B, A, b, c, obj, l, e)
            e = np.argmax(c)
        for mb in new_B:
            if mb >= self.var:
                row = mb - self.var
                i = 0
                while A[row][i] == 0 and i < self.var:
                    i += 1
                (new_B, A, b, c, obj) = self.hallar_pivote(new_B, A, b, c, obj, new_B.index(mb), i)
        return (new_B, A[:, 0:self.var], b)

    def simplex(self, A, b, c):
        B = ''
        (B, A, b) = self.inicializar_simplex(A, b)
        obj = np.dot(c[B], b)
        c = np.dot(c[B].reshape(1, -1), A) - c
        c = c[0]
        e = np.argmax(c)
        while c[e] > 0:
            theta = []
            for i in range(len(b)):
                if A[i][e] > 0:
                    theta.append(b[i] / A[i][e])
                else:
                    theta.append(Decimal("inf"))
            l = np.argmin(np.array(theta))
            if theta[l] == Decimal('inf'):
                print("unbounded")
                return False
            (B, A, b, c, obj) = self.hallar_pivote(B, A, b, c, obj, l, e)
            e = np.argmax(c)
        x = self.calcular_x(B, b)
        return (x, obj)

    def calcular_x(self, B, b):
        x = np.zeros(self.var, dtype=float)
        x[B] = b
        return x

         # Transformación base
    def hallar_pivote(self, B, A, b, c, z, l, e):
        # main element is a_le
        # l represents leaving basis
        # e represents entering basis
        main_elem = A[l][e]
        # scaling the l-th line
        A[l] = A[l] / main_elem
        b[l] = b[l] / main_elem
        # change e-th column to unit array
        for i in range(self.row):
            if i != l:
                b[i] = b[i] - A[i][e] * b[l]
                A[i] = A[i] - A[i][e] * A[l]
        # update objective value
        z -= b[l] * c[e]
        c = c - c[e] * A[l]
        # change the basis
        B[l] = e
        return (B, A, b, c, z)

s = Simplex()
s.solve()

c = np.array ([2,1,1], dtype=Decimal) # Coeficiente de función objetivo, vector de columna 3x1
A_ub = np.array ([[0,2, -1], [0,1, -1]], dtype=Decimal) # Coeficiente de restricción de desigualdad A, matriz de 2x3 dimensiones
B_ub = np.array ([- 2,1], dtype=Decimal) # Coeficiente de restricción de igualdad B, vector de columna dimensional 2x1
A_eq = np.array ([[1, -1,1]], dtype=Decimal) # Coeficiente de restricción de igualdad Aeq, vector de columna dimensional 3x1
B_eq = np.array ([2], dtype=Decimal) # coeficiente de restricción de ecuación beq, valor 1x1
res = op.linprog(c, A_ub, B_ub, A_eq, B_eq) # Función de llamada para resolver
print(res)

c = np.array ([300, 250, 450], dtype=Decimal) # Coeficiente de función objetivo, vector de columna 3x1
A_ub = np.array ([[15, 20, 25], [35, 60, 60], [20, 30, 25], [0, 250, 0]], dtype=Decimal) # Coeficiente de restricción de desigualdad A, matriz de 2x3 dimensiones
B_ub = np.array ([1200, 3000, 1500, 500], dtype=Decimal) # Coeficiente de restricción de igualdad B, vector de columna dimensional 2x1
A_eq = np.array ([[1, 1,1]], dtype=Decimal) # Coeficiente de restricción de igualdad Aeq, vector de columna dimensional 3x1
B_eq = np.array ([3], dtype=Decimal) # coeficiente de restricción de ecuación beq, valor 1x1
res = op.linprog (c, A_ub, B_ub, A_eq, B_eq) # Función de llamada para resolver
print(res)


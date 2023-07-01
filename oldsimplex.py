import numpy as np

class Simplex:
    
    MAX_NUMBER = 10 ** 18

    def __init__(self, r: int = 0, v: int = 0):
        self.R = r
        self.V = v
        self.matrix = []
        self.method = 0

    def create_matrix(self):
        self.matrix = np.zeros((self.R + 1, self.V + 2))
        self.matrix = np.array(
            [[float(input(f'Ingrese el valor {j+1} {k+1}: ')) for k in range(self.V+2)] for j in range(self.R+1)]
        )

    def simplex_method(self):
        print("Coloque 1 si es maximizacion o 2 si es minimizacion")
        self.method = int(input())
        if self.method == 1:
            self.simplex_method_for_maximization()
        else:
            self.simplex_method_for_minimization()

    def transform_row(self, ma0, r, idf):
        for i in range(0, self.R + 1):
            if i != np.argmin(r) + 1:
                ma0[i] = -(ma0[i][idf]) * ma0[np.argmin(r) + 1] + ma0[i]

    def simplex_method_for_maximization(self):
        ma0 = np.copy(self.matrix)
        while min(ma0[0]) < 0:
            # code for finding pivot
            idf = np.argmin(ma0[0])
            r = []
            for l in range(0, self.R):
                n = ma0[l + 1][self.V + 1]
                d = ma0[l + 1][idf]
                t = n / d if d != 0 else self.MAX_NUMBER
                r.append(self.MAX_NUMBER if t < 0 else t)
            ma0[np.argmin(r) + 1] = ma0[np.argmin(r) + 1] / ma0[np.argmin(r) + 1][idf]
            self.transform_row(ma0, r, idf)

    def simplex_method_for_minimization(self):
        ma0 = np.copy(self.matrix)
        while max(ma0[0]) > 0:
            # code for finding pivot
            idf = np.argmax(ma0[0])
            r = []
            for l in range(0,self.R):
                n= ma0[l+1][self.V+1]
                d= ma0[l+1][idf]
                t = n / d if d != 0 else self.MAX_NUMBER
                r.append(self.MAX_NUMBER if t < 0 else t)
            ma0[np.argmin(r)+1]=ma0[np.argmin(r)+1]/ma0[np.argmin(r)+1][idf]
            self.transform_row(ma0, r, idf)

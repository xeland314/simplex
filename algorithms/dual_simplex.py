import numpy as np
from typing import List, Tuple, Optional

class DualSimplex:
    def __init__(self, c: List[float], A: List[List[float]], b: List[float], maximize: bool = True):
        """
        Initialize Dual Simplex solver.
        c: coefficients of objective function
        A: constraint matrix (Ax <= b)
        b: right-hand side
        maximize: True for maximization, False for minimization
        """
        self.c = np.array(c, dtype=float)
        self.A = np.array(A, dtype=float)
        self.b = np.array(b, dtype=float)
        self.maximize = maximize
        if not maximize:
            self.c = -self.c  # Convert to maximization internally

        self.m, self.n = self.A.shape
        # Add slack variables
        self.slack_A = np.hstack([self.A, np.eye(self.m)])
        self.slack_c = np.concatenate([self.c, np.zeros(self.m)])
        self.basic_vars = list(range(self.n, self.n + self.m))  # Initial basic variables are slacks
        self.non_basic_vars = list(range(self.n))

        # Initial tableau
        self.tableau = np.zeros((self.m + 1, self.n + self.m + 1))
        self.tableau[:-1, :-1] = self.slack_A
        self.tableau[:-1, -1] = self.b
        self.tableau[-1, :self.n + self.m] = -self.slack_c
        self.tableau[-1, -1] = 0  # Objective value

    def solve(self) -> Tuple[Optional[np.ndarray], Optional[float]]:
        """
        Solve using Dual Simplex method.
        Returns: (optimal_solution, optimal_value) or (None, None) if unbounded/infeasible
        """
        while True:
            basic_values = self.tableau[:-1, -1]
            primal_feasible = np.all(basic_values >= -1e-10)  # Allow small tolerance

            if primal_feasible:
                # Check dual feasibility
                dual_feasible = all(self.tableau[-1, j] >= -1e-10 for j in self.non_basic_vars)
                if dual_feasible:
                    # Optimal solution found
                    solution = np.zeros(self.n)
                    for i, var in enumerate(self.basic_vars):
                        if var < self.n:
                            solution[var] = basic_values[i]
                    optimal_value = self.tableau[-1, -1] if self.maximize else -self.tableau[-1, -1]
                    return solution, optimal_value

                else:
                    # Primal feasible, dual not: do primal pivot
                    # Choose entering variable: most negative c_j
                    entering_candidates = [(self.tableau[-1, j], j) for j in self.non_basic_vars if self.tableau[-1, j] < -1e-10]
                    if not entering_candidates:
                        # Unbounded
                        return None, None
                    entering_var = min(entering_candidates)[1]

                    # Choose leaving variable: min ratio b_i / a_{i j} for a_{i j} > 0
                    ratios = []
                    for i in range(self.m):
                        a_ij = self.tableau[i, entering_var]
                        if a_ij > 1e-10:
                            ratio = basic_values[i] / a_ij
                            ratios.append((ratio, i))
                    if not ratios:
                        # Unbounded
                        return None, None
                    leaving_row = min(ratios)[1]
                    self._pivot(leaving_row, entering_var)

            else:
                # Primal not feasible: do dual pivot
                # Choose leaving variable: most negative b_i
                leaving_row = np.argmin(basic_values)
                leaving_var = self.basic_vars[leaving_row]

                # Choose entering variable
                row = self.tableau[leaving_row, :-1]
                ratios = []
                for j in self.non_basic_vars:
                    if row[j] < -1e-10:  # Only consider negative coefficients
                        ratio = self.tableau[-1, j] / row[j]
                        ratios.append((ratio, j))
                if not ratios:
                    # Infeasible
                    return None, None
                entering_var = min(ratios)[1]

                # Pivot
                self._pivot(leaving_row, entering_var)

    def _pivot(self, row: int, col: int):
        """
        Perform pivot operation.
        """
        pivot_element = self.tableau[row, col]
        self.tableau[row, :] /= pivot_element

        for i in range(self.tableau.shape[0]):
            if i != row:
                factor = self.tableau[i, col]
                self.tableau[i, :] -= factor * self.tableau[row, :]

        # Update basic and non-basic variables
        self.basic_vars[row], self.non_basic_vars[self.non_basic_vars.index(col)] = col, self.basic_vars[row]

from advanced_simplex import Simplex
from functions import AlgebraicExpression, ObjectiveFunction

class Expression:
    def __init__(self, terms=None, const=0):
        self.terms = terms if terms else {}
        self.const = const

    def __neg__(self):
        new_terms = {var: -coef for var, coef in self.terms.items()}
        return Expression(new_terms, -self.const)

    def __add__(self, other):
        new_terms = self.terms.copy()
        if isinstance(other, Expression):
            for var, coef in other.terms.items():
                new_terms[var] = new_terms.get(var, 0) + coef
            return Expression(new_terms, self.const + other.const)
        else:
            return Expression(new_terms, self.const + other)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        new_terms = self.terms.copy()
        if isinstance(other, Expression):
            for var, coef in other.terms.items():
                new_terms[var] = new_terms.get(var, 0) - coef
            return Expression(new_terms, self.const - other.const)
        else:
            return Expression(new_terms, self.const - other)

    def __rsub__(self, other):
        expr = self.__sub__(other)
        expr.const *= -1
        for var in expr.terms:
            expr.terms[var] *= -1
        return expr

    def __mul__(self, other):
        new_terms = {var: coef * other for var, coef in self.terms.items()}
        return Expression(new_terms, self.const * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __le__(self, other):
        return (self, "<=", other)

    def __ge__(self, other):
        return (self, ">=", other)

    def __eq__(self, other):
        return (self, "==", other)

class Var(Expression):
    def __init__(self, name, low=None, cat='Continuous'):
        super().__init__({name: 1})
        self.name = name
        self.low = low
        self.cat = cat

class Model:
    def __init__(self, name=""):
        self.name = name
        self.objective = None
        self.constraints = []
        self.vars = {}

    def __iadd__(self, other):
        if isinstance(other, tuple):
            if len(other) == 2 and other[0] in ['maximize', 'minimize']:
                self.objective = other
            else:
                self.constraints.append(other)
        return self

    def solve(self):
        sense, obj_expr = self.objective
        obj_func_str = f"z = {self._expr_to_str(obj_expr)}"
        objective_function = ObjectiveFunction(obj_func_str)

        constraints = []
        for left, op, right in self.constraints:
            right_expr = Expression(const=right) if not isinstance(right, Expression) else right
            expr = left - right_expr
            const_str = f" {op} {expr.const * -1}"
            constraints.append(AlgebraicExpression(self._expr_to_str(expr) + const_str))

        # Collect all variables
        all_vars = set(objective_function.variables)
        for c in constraints:
            all_vars.update(c.variables)

        simplex = Simplex(
            num_variables=len(all_vars),
            objective_function=objective_function,
            method=Simplex.MAXIMIZE if sense == 'maximize' else Simplex.MINIMIZE,
            constraints=constraints,
        )
        simplex.solve_problem()
        return simplex
    
    def _expr_to_str(self, expr):
        terms = []
        for var, coef in expr.terms.items():
            if coef == 1:
                terms.append(var)
            elif coef == -1:
                terms.append(f"- {var}")
            else:
                terms.append(f"{coef} * {var}")
        return " + ".join(terms).replace("+ -", "-")

def maximize(expr):
    return ("maximize", expr)

def minimize(expr):
    return ("minimize", expr)
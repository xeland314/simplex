from decimal import Decimal, ROUND_HALF_UP
import os
from typing import Optional

from rich.console import Console
from rich.table import Table
from scipy.optimize import linprog

from functions import AlgebraicExpression, ObjectiveFunction

clear_terminal = lambda: os.system('cls' if os.name == 'nt' else 'clear')

class Simplex:

    MINIMIZE: int = 0
    MAXIMIZE: int = 1
    PRECISION = Decimal('0.000001')
    DEFAULT_VARIABLE: str = "s"

    def __init__(self,
        num_variables = 0,
        objective_function: Optional[ObjectiveFunction] = None,
        method: int = MAXIMIZE | MINIMIZE,
        constraints: list[AlgebraicExpression] = []
    ):
        if objective_function is None:
            return
        self.num_variables = num_variables
        self.objective_function: ObjectiveFunction = objective_function
        self.method = method
        self.num_constraints = len(constraints)
        self.constraints = constraints
        self.A, self.b, self.c = [], [], []

    def __call__(self):
        self.__enter_num_variables()
        self.__enter_objective_function()
        self.__select_method()
        self.__enter_num_constraints()
        self.__enter_constraints()
        self.solve_problem()
        self.show_results()

    def __enter_num_variables(self) -> None:
        while(self.num_variables <= 0):
            clear_terminal()
            try:
                self.num_variables = int(
                    input("Enter the number of variables: ")
                )
            except Exception:
                pass

    def __enter_objective_function(self) -> None:
        entry: str = ""
        while(not ObjectiveFunction.is_an_objective_function(entry)):
            clear_terminal()
            print("Function format: z = ax1 + bx2 + ... + cxn")
            print("a, b, c are numbers.")
            entry = input("Enter the objective function: ")
        self.objective_function = ObjectiveFunction(entry)

    def __complete_objective_function(self) -> None:
        if self.objective_function.number_of_variables != self.num_variables:
            missing_variables = self.num_variables - self.objective_function.number_of_variables
            for value in range(missing_variables):
                self.objective_function.ordered_variables.append(
                    f"{self.DEFAULT_VARIABLE}{value + 1}"
                )

    def __select_method(self) -> None:
        while(not(self.method == self.MAXIMIZE or self.method == self.MINIMIZE)):
            clear_terminal()
            try:
                self.method = int(
                    input("Do you want to maximize (1) or minimize (0) the objective function?: ")
                )
            except Exception:
                pass

    def __enter_num_constraints(self) -> None:
        while(self.num_constraints <= 0):
            clear_terminal()
            try:
                self.num_constraints = int(
                    input("Enter the number of constraints: ")
                )
            except Exception:
                pass

    def __enter_constraints(self) -> None:
        for r in range(self.num_constraints):
            entry: str = ""
            while(not AlgebraicExpression.is_an_algebraic_expression(entry)):
                clear_terminal()
                print("Constraint format: ax1 + bx2 + ... + cxn = d")
                print("a, b, c, d are numbers.")
                entry = input(f"Enter constraint #{r + 1}: ")
            self.constraints.append(
                AlgebraicExpression(entry)
            )
        clear_terminal()

    def __complete_constraints(self) -> None:
        for constraint in self.constraints:
            if constraint.variables == self.objective_function.variables:
                continue
            constraint.ordered_variables = self.objective_function.variables

    def __verify_constraints(self) -> None:
        variables_f = set(self.objective_function.variables)
        for constraint in self.constraints:
            variables_r = set(constraint.variables)
            if not variables_r.issubset(variables_f):
                variables = variables_r.difference(variables_f)
                raise ValueError(
                    f"The variable{{'s' if len(variables) > 1 else ''}} {variables} "
                    f"of the constraint {constraint} "
                    f"does not exist{{'s' if len(variables) > 1 else ''}} "
                    f"in the objective function: {self.objective_function}.\n"
                    "Cannot continue with the execution of the program."
                )

    def __prepare_data(self) -> None:
        self.__complete_objective_function()
        self.__verify_constraints()
        self.__complete_constraints()
        self.A.clear(), self.b.clear()
        self.c = self.objective_function.coefficients
        if self.method == self.MAXIMIZE:
            self.c = [-ci for ci in self.c]
        for constraint in self.constraints:
            row = constraint.coefficients
            sign = constraint.sign
            if sign == '<=':
                # the constraint is of type Ax <= b
                self.A.append(row)
                self.b.append(constraint.independent_term)
            elif sign == '>=':
                # the constraint is of type Ax >= b,
                # everything is multiplied by -1
                self.A.append([-aij for aij in row])
                self.b.append(-constraint.independent_term)
            elif sign == '<':
                # the constraint is of type Ax < b,
                # a small value is subtracted from b
                # to turn it into Ax <= b - epsilon
                self.A.append(row)
                self.b.append(constraint.independent_term - Decimal("1e-6"))
            elif sign == '>':
                # the constraint is of type Ax > b,
                # everything is multiplied by -1
                # and a small value is subtracted from b
                # to turn it into -Ax <= -b + epsilon
                self.A.append([-aij for aij in row])
                self.b.append(-constraint.independent_term + Decimal("1e-6"))
            elif sign == '=':
                # the constraint is of type Ax = b
                self.A.append(row)
                self.b.append(constraint.independent_term)
                # add constraint of type -Ax <= -b
                self.A.append([-aij for aij in row])
                self.b.append(-self.b[-1])

    def print_problem(self) -> None:
        title = (
            f"{ 'Maximize' if self.method == self.MAXIMIZE else 'Minimize'} "
            f"[dark_blue]{self.objective_function}[/dark_blue]"
        )
        table = Table(title=title, title_justify="left")
        table.add_column(header="Constraints", justify="left", style="deep_sky_blue3")
        table.add_column(header=f"{self.objective_function.variables}", justify="center", style="green")
        table.add_column(header="<=>", justify="center", style="deep_pink3")
        table.add_column(header="b", justify="center", style="green")
        for constraint in self.constraints:
            table.add_row(
                str(constraint),
                str([str(value) for value in constraint.coefficients]),
                constraint.sign,
                str(constraint.independent_term)
            )
        console = Console()
        console.print(table)

    def solve_problem(self) -> None:
        self.__prepare_data()
        # Define the bounds of the variables
        self.bounds = [(0, None) for _ in range(self.num_variables)]
        # Solve the linear programming problem
        self.response = linprog(
            self.c, A_ub=self.A, b_ub=self.b,
            bounds=self.bounds, method='highs'
        )

        #Save optimal values
        self.optimal_values = []
        value = -self.response.fun if self.method == self.MAXIMIZE else self.response.fun
        value = Decimal(value).quantize(self.PRECISION, ROUND_HALF_UP)
        self.optimal_values.append((self.objective_function.function_name, value.normalize()))
        for variable, value in zip(self.objective_function.variables, self.response.x):
            value = Decimal(value).quantize(self.PRECISION, ROUND_HALF_UP)
            self.optimal_values.append((variable, value.normalize()))

    def __show_prepared_data(self) -> None:
        table = Table(title="Data Preparation", title_justify="center")
        table.add_column(header="A", justify="left", style="deep_sky_blue3")
        table.add_column(header="b", justify="right", style="deep_sky_blue3")
        for row, value in zip(self.A, self.b):
            table.add_row(str([str(value) for value in row]), str(value))
        c_values = [str(value) for value in self.c]
        table.add_section()
        table.add_row(str(c_values),"0")
        console = Console()
        console.print(table)

    def show_results(self) -> None:
        self.print_problem()
        self.__show_prepared_data()
        if not self.response.success:
            print('Could not find an optimal solution.')
            return
        # Print result if an optimal solution was found
        table = Table(title="Results", title_justify="center")
        table.add_column(header="Variables", justify="center", style="magenta")
        table.add_column(header="Optimal values", justify="left", style="green")
        for variable, value in self.optimal_values:
            table.add_row(variable, str(value))
        console = Console()
        console.print(table)

if __name__ == "__main__":
    run_simplex = Simplex()
    run_simplex()
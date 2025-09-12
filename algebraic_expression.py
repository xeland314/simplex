from decimal import Decimal
import re
from math_expression import MathExpression

class AlgebraicExpression(MathExpression):
    """
    Represents an algebraic equation or inequality.

    This class parses a string to extract its coefficients, variables,
    sign (e.g., '=', '<='), and the independent term.
    """


    def __init__(self, expression: str) -> None:
        super().__init__(expression)
        self._parse_expression()
        self._generate_representation()

    def _generate_representation(self) -> None:
        self.representation = ""
        terms_str = []
        for variable, coefficient in self.terms.items():
            if coefficient == 1:
                terms_str.append(f"{variable}")
            elif coefficient == -1:
                terms_str.append(f"-{variable}")
            elif coefficient < 0:
                terms_str.append(f"-{-coefficient} * {variable}")
            else:
                terms_str.append(f"{coefficient} * {variable}")
        self.representation = " + ".join(terms_str)
        self.representation = self.representation.replace(" + -", " - ")
        self.representation += f" {self.sign} {self.independent_term}"

    def _parse_expression(self) -> None:
        """
        Parses a given equation or inequality as a string and finds
        its coefficients, variable names, sign, and independent term.

        Args:
            - expression (str): A string representing an equation or inequality.
                - The equation must be in the form: "ax1 + bx2 + ... + cxn = d" or "ax1 + bx2 + ... + cxn <= d",
                - where a, b, c, ... are coefficients and
                - d is the independent term.
                - The sign can be "=", "<=", ">=", "<" or ">".
        """
        # Split the equation into two parts: left and right side
        left_side, right_side = re.split(r'[<>=]=?', self.expression)

        # Get the equality or inequality sign
        self.sign: str = re.findall(r'[<>=]=?', self.expression)[0]

        # Get the coefficients and variable names from the left side
        for term in re.findall(r'([+-]?\s*\d*\.?\d*\s*\*?)\s*(\w+)', left_side):
            coefficient, variable = term
            coefficient: str = coefficient.replace(' ', '').replace('*', '')
            if coefficient not in ['', '+', '-']:
                self.terms[variable] += Decimal(coefficient)
            else:
                self.terms[variable] += Decimal((coefficient if coefficient else '+') + '1')
            if variable not in self.ordered_variables:
                self.ordered_variables.append(variable)

        # Get the independent term from the right side
        self.independent_term = Decimal(right_side.strip())

    @staticmethod
    def is_an_algebraic_expression(expression: str) -> bool:
        """
        Determines if a given string represents a valid algebraic expression.

        Args:
            - expression(str): A string representing a possible algebraic expression.

        Returns:
            - bool: True if the string represents a valid algebraic expression,
            False otherwise.
        """
        pattern = r'^\s*[+-]?\s*\d*\s*\*?\s*\w+\s*([+-]\s*\d*\s*\*?\s*\w+\s*)*([<>=]=?)\s*[+-]?\d+\s*$'
        return bool(re.match(pattern, expression))

    def __repr__(self) -> str:
        return f"AlgebraicExpression({self.representation})"

    def __str__(self) -> str:
        return self.representation
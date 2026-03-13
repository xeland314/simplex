from abc import ABCMeta, abstractmethod
from collections import Counter


class MathExpression(metaclass=ABCMeta):
    """
    An abstract base class for mathematical expressions.

    This class provides the fundamental structure and properties for handling
    mathematical expressions, including parsing and representation.
    """

    def __init__(self, expression: str) -> None:
        """
        Initializes a MathExpression object.

        Args:
            expression (str): The string representation of the mathematical expression.
        """
        self.expression = expression
        self.terms = Counter()
        self.ordered_variables = []

    @property
    def coefficients(self) -> list:
        """
        Gets the coefficients of the variables in the expression.

        The coefficients are returned in the same order as the variables
        were first encountered during parsing.

        Returns:
            list: A list of coefficients (Decimal values).
        """
        coefficients = []
        for variable in self.ordered_variables:
            value = self.terms.get(variable, 0)
            coefficients.append(value)
        return coefficients

    @property
    def number_of_variables(self) -> int:
        """
        Gets the number of unique variables in the expression.

        Returns:
            int: The count of unique variables.
        """
        return len(self.ordered_variables)

    @property
    def variables(self) -> list:
        """
        Gets the list of unique variables in the expression, in the order they were parsed.

        Returns:
            list: A list of variable names (strings).
        """
        return self.ordered_variables

    @abstractmethod
    def _generate_representation(self) -> None:
        """
        Generates the formatted string representation of the expression.

        This is an abstract method that must be implemented by subclasses.
        """

    @abstractmethod
    def _parse_expression(self) -> None:
        """
        Parses the string expression to populate terms, variables, and other attributes.

        This is an abstract method that must be implemented by subclasses.
        """
import re


# -------------------------------
# Custom Exceptions
# -------------------------------

class InvalidFormatError(Exception):
    pass


class UnknownVariableError(Exception):
    pass


class DivisionByZeroError(Exception):
    pass


class UnsupportedOperatorError(Exception):
    pass


# -------------------------------
# Helper Functions
# -------------------------------

def get_value(token, variables):
    """
    Convert token into a number or retrieve
    the value of a stored variable.
    """

    # Integer or decimal
    try:
        return float(token)
    except ValueError:
        pass

    # Variable name
    if re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', token):

        if token in variables:
            return variables[token]

        raise UnknownVariableError(
            f"Unknown variable: {token}"
        )

    raise InvalidFormatError(
        f"Invalid operand: {token}"
    )


def calculate(left, operator, right):
    """Perform the requested operation."""

    if operator == "+":
        return left + right

    elif operator == "-":
        return left - right

    elif operator == "*":
        return left * right

    elif operator == "/":
        if right == 0:
            raise DivisionByZeroError(
                "Cannot divide by zero"
            )

        return left / right

    elif operator == "%":
        if right == 0:
            raise DivisionByZeroError(
                "Cannot perform modulo by zero"
            )

        return left % right

    else:
        raise UnsupportedOperatorError(
            f"Unsupported operator: {operator}"
        )


def format_result(value):
    """Print integers without .0."""

    if value.is_integer():
        return str(int(value))

    return str(value)


# -------------------------------
# Main Calculator
# -------------------------------

def main():

    variables = {}

    while True:

        try:
            line = input().strip()

        except EOFError:
            break

        if not line:
            continue

        if line.lower() == "quit":
            break

        try:

            # Assignment:
            # x = 10
            if "=" in line:

                parts = line.split("=")

                if len(parts) != 2:
                    raise InvalidFormatError(
                        "Invalid assignment format"
                    )

                variable = parts[0].strip()
                value_token = parts[1].strip()

                # Check variable name
                if not re.fullmatch(
                    r'[A-Za-z_][A-Za-z0-9_]*',
                    variable
                ):
                    raise InvalidFormatError(
                        "Invalid variable name"
                    )

                # Assignment value
                value = get_value(
                    value_token,
                    variables
                )

                variables[variable] = value

                continue

            # Formula must contain exactly 3 parts
            parts = line.split()

            if len(parts) != 3:
                raise InvalidFormatError(
                    "Expected: operand operator operand"
                )

            left_token = parts[0]
            operator = parts[1]
            right_token = parts[2]

            # Only these operators are allowed
            if operator not in ["+", "-", "*", "/", "%"]:
                raise UnsupportedOperatorError(
                    f"Unsupported operator: {operator}"
                )

            left = get_value(
                left_token,
                variables
            )

            right = get_value(
                right_token,
                variables
            )

            result = calculate(
                left,
                operator,
                right
            )

            print(format_result(result))

        except (
            InvalidFormatError,
            UnknownVariableError,
            DivisionByZeroError,
            UnsupportedOperatorError
        ) as e:

            print(type(e).__name__)

            # If meaningful message is required:
            # print(type(e)._name_, ":", e)


if __name__ == "__main__":
    main()
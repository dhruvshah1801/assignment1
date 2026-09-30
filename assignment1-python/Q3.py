import re

class ExpressionParser:
    def __init__(self, text, variables, memo, visiting):
        self.text = text
        self.variables = variables
        self.memo = memo
        self.visiting = visiting
        self.pos = 0

    def skip_spaces(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

    def parse(self):
        value = self.parse_expression()

        self.skip_spaces()

        if self.pos != len(self.text):
            raise ValueError("Invalid syntax")

        return value

    def parse_expression(self):
        value = self.parse_term()

        while True:
            self.skip_spaces()

            if self.pos < len(self.text) and self.text[self.pos] == '+':
                self.pos += 1
                value += self.parse_term()

            elif self.pos < len(self.text) and self.text[self.pos] == '-':
                self.pos += 1
                value -= self.parse_term()

            else:
                break

        return value

    def parse_term(self):
        value = self.parse_factor()

        while True:
            self.skip_spaces()

            if self.pos < len(self.text) and self.text[self.pos] == '*':
                self.pos += 1
                value *= self.parse_factor()
            else:
                break

        return value

    def parse_factor(self):
        self.skip_spaces()

        if self.pos >= len(self.text):
            raise ValueError("Invalid expression")

        # Parentheses
        if self.text[self.pos] == '(':
            self.pos += 1

            value = self.parse_expression()

            self.skip_spaces()

            if self.pos >= len(self.text) or self.text[self.pos] != ')':
                raise ValueError("Missing closing parenthesis")

            self.pos += 1
            return value

        # Number
        if self.text[self.pos].isdigit():
            start = self.pos

            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                self.pos += 1

            return int(self.text[start:self.pos])

        # Variable
        if self.text[self.pos].isalpha() or self.text[self.pos] == '_':
            start = self.pos

            while (
                self.pos < len(self.text)
                and (self.text[self.pos].isalnum() or self.text[self.pos] == '_')
            ):
                self.pos += 1

            name = self.text[start:self.pos]

            return evaluate_variable(
                name,
                self.variables,
                self.memo,
                self.visiting
            )

        raise ValueError("Invalid character")


def evaluate_variable(name, variables, memo, visiting):
    # Already calculated
    if name in memo:
        return memo[name]

    # Variable does not exist
    if name not in variables:
        raise ValueError("Undefined variable")

    # Cycle detected
    if name in visiting:
        raise RuntimeError("CYCLE")

    visiting.add(name)

    parser = ExpressionParser(
        variables[name],
        variables,
        memo,
        visiting
    )

    value = parser.parse()

    visiting.remove(name)

    # Store calculated value
    memo[name] = value

    return value


def main():
    try:
        v = int(input().strip())

        variables = {}

        for _ in range(v):
            line = input().strip()

            if '=' not in line:
                print("INVALID")
                return

            name, expression = line.split('=', 1)

            name = name.strip()
            expression = expression.strip()

            if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', name):
                print("INVALID")
                return

            variables[name] = expression

        final_expression = input().strip()

        memo = {}
        visiting = set()

        parser = ExpressionParser(
            final_expression,
            variables,
            memo,
            visiting
        )

        answer = parser.parse()

        print(answer)

    except RuntimeError as e:
        if str(e) == "CYCLE":
            print("CYCLE")
        else:
            print("INVALID")

    except Exception:
        print("INVALID")


if __name__ == "__main__":
    main()
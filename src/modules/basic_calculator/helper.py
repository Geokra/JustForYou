def calculate(expression: str) -> float:
        pos = 0  # current character index, shared across all inner functions

        def peek() -> str | None:
            return expression[pos] if pos < len(expression) else None

        def consume() -> str:
            nonlocal pos
            ch = expression[pos]
            pos += 1
            return ch

        def skip_whitespace():
            nonlocal pos
            while pos < len(expression) and expression[pos] == ' ':
                pos += 1

        def parse_number() -> float:
            nonlocal pos
            skip_whitespace()
            start = pos
            if peek() == '-':
                consume()
            while peek() is not None and (peek().isdigit() or peek() == '.'):
                consume()
            if pos == start:
                raise ValueError(f"Expected number at position {pos}, got {peek()!r}")
            return float(expression[start:pos])

        def parse_atom() -> float:
            """Handles numbers, unary minus, and parenthesised groups."""
            skip_whitespace()
            if peek() == '(':
                consume()  # '('
                result = parse_expr()
                skip_whitespace()
                if peek() != ')':
                    raise ValueError(f"Expected ')' at position {pos}, got {peek()!r}")
                consume()  # ')'
                return result
            elif peek() == '-':
                consume()
                return -parse_atom()
            else:
                return parse_number()

        def parse_power() -> float:
            """Handles ** (right-associative)."""
            nonlocal pos  # already nonlocal via outer scope
            base = parse_atom()
            skip_whitespace()
            if pos + 1 < len(expression) and expression[pos:pos+2] == '**':
                pos += 2
                exp = parse_power()  # right-associative: recurse
                return base ** exp
            return base

        def parse_term() -> float:
            """Handles * and /."""
            left = parse_power()
            while True:
                skip_whitespace()
                op = peek()
                if op == '*' and expression[pos:pos+2] != '**':
                    consume()
                    left *= parse_power()
                elif op == '/':
                    consume()
                    divisor = parse_power()
                    if divisor == 0:
                        raise ValueError("Division by zero")
                    left /= divisor
                else:
                    break
            return left

        def parse_expr() -> float:
            """Handles + and - (lowest precedence)."""
            left = parse_term()
            while True:
                skip_whitespace()
                op = peek()
                if op == '+':
                    consume()
                    left += parse_term()
                elif op == '-':
                    consume()
                    left -= parse_term()
                else:
                    break
            return left

        result = parse_expr()
        skip_whitespace()

        if pos != len(expression):
            raise ValueError(f"Unexpected character at position {pos}: {expression[pos]!r}")

        return result
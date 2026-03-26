"""Proprietaere mathematische Funktionen – keine externen Bibliotheken."""


def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("n muss >= 0 sein")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def sqrt(x: float, precision: float = 1e-12) -> float:
    """Quadratwurzel nach dem Heron-Verfahren (Newton)."""
    if x < 0:
        raise ValueError("Zahl darf nicht negativ sein")
    if x == 0:
        return 0.0
    guess = x if x >= 1 else 1.0
    while True:
        next_guess = (guess + x / guess) / 2.0
        if abs(next_guess - guess) < precision:
            return next_guess
        guess = next_guess


def gcd(a: int, b: int) -> int:
    """Groesster gemeinsamer Teiler (Euklidischer Algorithmus)."""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def simplify_fraction(numerator: int, denominator: int) -> tuple[int, int]:
    """Kuerzt einen Bruch auf die einfachste Form."""
    if denominator == 0:
        raise ValueError("Nenner darf nicht 0 sein")
    if numerator == 0:
        return 0, 1
    sign = -1 if (numerator < 0) != (denominator < 0) else 1
    numerator, denominator = abs(numerator), abs(denominator)
    d = gcd(numerator, denominator)
    return sign * (numerator // d), denominator // d


def decimal_to_fraction(value: float) -> tuple[int, int]:
    """Wandelt eine Dezimalzahl in einen gekuerzten Bruch um."""
    if value == int(value):
        return int(value), 1

    text = f"{value:.15g}"
    if "." in text:
        decimals = len(text.split(".")[1])
    else:
        decimals = 0

    denominator = 1
    for _ in range(decimals):
        denominator *= 10

    numerator = round(value * denominator)
    return simplify_fraction(numerator, denominator)


def power(base: float, exponent: float) -> float:
    """Potenzfunktion fuer rationale Exponenten."""
    if base == 0:
        if exponent < 0:
            raise ValueError("Division durch 0 (0 hoch negativer Exponent)")
        if exponent == 0:
            return 1.0
        return 0.0

    # Ganzzahliger Exponent: iterativ
    if exponent == int(exponent):
        return _int_power(base, int(exponent))

    # Rationaler Exponent: base^(p/q) = q-te Wurzel von base^p
    # Nutze Annaeherung ueber exp/ln
    if base < 0:
        raise ValueError("Negative Basis mit nicht-ganzzahligem Exponent nicht definiert")

    return _exp(_ln(base) * exponent)


def _int_power(base: float, exp: int) -> float:
    """Ganzzahlige Potenz per Exponentiation by Squaring."""
    if exp < 0:
        base = 1.0 / base
        exp = -exp
    result = 1.0
    while exp > 0:
        if exp % 2 == 1:
            result *= base
        base *= base
        exp //= 2
    return result


def _ln(x: float, iterations: int = 200) -> float:
    """Natuerlicher Logarithmus ueber Reihenentwicklung."""
    if x <= 0:
        raise ValueError("ln nur fuer positive Zahlen definiert")

    # Bereichsreduktion: x = m * 2^k, ln(x) = ln(m) + k*ln(2)
    k = 0
    m = x
    ln2 = 0.6931471805599453  # Vorberechnet, da Konstante
    while m > 2.0:
        m /= 2.0
        k += 1
    while m < 0.5:
        m *= 2.0
        k -= 1

    # Reihe fuer ln((1+t)/(1-t)) = 2*(t + t^3/3 + t^5/5 + ...)
    # mit t = (m-1)/(m+1)
    t = (m - 1.0) / (m + 1.0)
    t2 = t * t
    result = 0.0
    term = t
    for i in range(iterations):
        result += term / (2 * i + 1)
        term *= t2
    return 2.0 * result + k * ln2


def _exp(x: float, terms: int = 50) -> float:
    """Exponentialfunktion ueber Taylor-Reihe."""
    result = 1.0
    term = 1.0
    for i in range(1, terms):
        term *= x / i
        result += term
        if abs(term) < 1e-15:
            break
    return result

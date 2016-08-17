import fractions
import functools
import itertools as it
import math
import operator


def rationalize(f):
    """Allow a single argument function to accept a Fraction or a numerator and denominator."""
    def g(x, denominator=None, **kwargs):
        if denominator: x = fractions.Fraction(x, denominator)
        return f(x, **kwargs)
    return g

def iterize(f):
    """Turn first argument of function into an iterator."""
    def g(x, *args, **kwargs):
        return f(iter(x), *args, **kwargs)
    return g


def integer_as_digits(n, base=10):
    k = 1
    while k * base < n:
        k *= base
    while k:
        yield n // k
        n = n % k
        k //= base

@rationalize
def rational_as_digits(x, base=10):
    x_digits = math.floor(x)
    yield from integer_as_digits(x_digits, base=base)
    yield '.'

    k = base
    while x != x_digits:
        yield math.floor(k * (x - x_digits))
        x_digits = fractions.Fraction(math.floor(k * x), k)
        k *= base


@rationalize
def continued_rational(x):
    while True:
        a = math.floor(x)
        yield a
        x -= a
        if not x: break
        x = 1 / x

@iterize
def continued_digits(digits, base=10):
    # integer part
    x = 0
    for d in digits:
        if d == '.': break
        x *= base
        x += d
    yield x
    n = 1

    # fractional part
    k = 1
    for d in digits:
        k *= base
        y = x + fractions.Fraction(d + 1, k)  # upper bound
        x = x + fractions.Fraction(d + 0, k)  # lower bound
        y_coefficients = continued_rational(y)
        x_coefficients = continued_rational(x)
        for a_x, a_y in it.islice(zip(x_coefficients, y_coefficients), n, None):
            if a_x == a_y:
                yield a_x
                n += 1
            else: break

    # leftovers
    yield from it.islice(continued_rational(x), n, None)

@iterize
def as_rational(coefficients):
    h_prev, k_prev = 0, 1
    h, k = 1, 0
    for a in coefficients:
        h, h_prev = a*h + h_prev, h
        k, k_prev = a*k + k_prev, k
    return fractions.Fraction(h, k)

@iterize
def as_digits(coefficients, base=10):
    # integer part
    x_digits = next(coefficients)
    yield from integer_as_digits(x_digits, base=base)
    yield '.'

    # continued part
    k = base
    x_coefficients = [x_digits]
    x = x_digits
    for a in coefficients:
        y_coefficients = x_coefficients + [a + 1]  # upper/lower bound
        x_coefficients = x_coefficients + [a + 0]  # lower/upper bound
        y = as_rational(y_coefficients)
        x = as_rational(x_coefficients)
        if math.floor(k * x) == math.floor(k * y):
            yield math.floor(k * (x - x_digits))
            x_digits = fractions.Fraction(math.floor(k * x), k)
            k *= base

    # rational part
    if x_digits != x:
        y = k * (x - x_digits) / base
        # slice off initial 0 and '.':
        yield from it.islice(rational_as_digits(y, base=base), 2, None)

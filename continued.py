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


def readints():
    import sys
    while True:
        line = sys.stdin.readline().strip()
        if line == '.': yield line
        elif line: yield int(line)
        else: break

def main():
    # 123456/1000 = 123.456 = [123;2,5,5,2]
    # 100/3 = 3.333… = [3;3]
    # 1900/99 = 19.191919… = [19;5,4,1,3]
    # ϕ = [1;1,1,1,…]
    for coefficients in ((123,2,5,5,2), (3,3), (19,5,4,1,3), it.cycle((1,))):
        print('coefficients:', ' '.join(map(str, it.islice(coefficients, 10))))
        rational = as_rational(it.islice(coefficients, 10))
        print('rational:', rational)
        print('rational digits:', ' '.join(map(str, it.islice(rational_as_digits(rational), 20))))
        print('rational coefficients:', ' '.join(map(str, continued_rational(rational))))
        print('digits:', ' '.join(map(str, it.islice(as_digits(coefficients), 20))))
        print('digit coefficients:', ' '.join(map(str, continued_digits(it.islice(as_digits(coefficients), 20)))))
        print()

    import random
    import statistics
    import matplotlib.pyplot as plt
    from tqdm import tqdm
    for n in (10, 100):
        means = []
        for _ in tqdm(range(100)):
            x = fractions.Fraction(sum(random.randrange(10) * 10**i for i in range(n)), 10**n)
            coefficients = list(it.islice(continued_rational(x), 1, None))
            means.append(math.exp(sum(map(math.log, coefficients)) / len(coefficients)))
        print('average geometric mean of coefficients of {} random digits:'.format(n),
              statistics.mean(means))
        plt.hist(means, label=str(n))
    plt.legend()
    plt.show()

    n = 100
    for base in (2, 10, 16):
        print('base:', base)
        n_digits = 0
        n_coefficients = -1
        xs = []
        ys = []
        def coefficients():
            nonlocal n_coefficients
            while True:
                n_coefficients += 1
                yield 1
        for _ in it.islice(tqdm(as_digits(coefficients(), base=base), total=n), 2, n):
            n_digits += 1
            xs.append(n_coefficients)
            ys.append(n_digits)
        print('ϕ digits per coefficient:', n_digits / n_coefficients)
        plt.plot(xs, ys, label='ϕ')

        for _ in range(3):
            n_digits = 0
            n_coefficients = -1
            xs = []
            ys = []
            def digits():
                nonlocal n_digits
                yield 0
                yield '.'
                while True:
                    n_digits += 1
                    yield random.randrange(base)
            for _ in continued_digits(tqdm(it.islice(digits(), n+2), total=n+2), base=base):
                n_coefficients += 1
                xs.append(n_coefficients)
                ys.append(n_digits)
                if n_digits == n: break
            print('random digits per coefficient:', n_digits / n_coefficients)
            plt.plot(xs, ys, label='random')

        plt.axes().set_aspect('equal')
        plt.legend()
        plt.show()

    print('enter digit or . per line, finish with empty line:')
    coefficients = []
    for a in continued_digits(readints()):
        coefficients.append(a)
        print(coefficients)

    print('enter coefficient per line, finish with empty line:')
    digits = []
    for d in as_digits(readints()):
        digits.append(d)
        print(' '.join(map(str, digits)))

if __name__ == '__main__':
    main()

import itertools as it
import random
import statistics

import matplotlib; matplotlib.rcParams['svg.fonttype'] = 'none'
import matplotlib.pyplot as plt
from tqdm import tqdm

from continued import *


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


# Lochs' constant:
base = 10
n = 1000

n_digits = 0
n_coefficients = -1
xs = []
ys = []
def phi_coefficients():
    global n_coefficients
    while True:
        n_coefficients += 1
        yield 1
for _ in tqdm(it.islice(as_digits(phi_coefficients(), base=base), 2, n), total=n-2):
    n_digits += 1
    xs.append(n_coefficients)
    ys.append(n_digits)
print('ϕ digits per coefficient:', n_digits / n_coefficients)
plt.plot(xs, ys, label='ϕ')

n_digits = 0
n_coefficients = -1
xs = []
ys = []
def sqrt2_coefficients():
    global n_coefficients
    n_coefficients += 1
    yield 1
    while True:
        n_coefficients += 1
        yield 2
for _ in tqdm(it.islice(as_digits(sqrt2_coefficients(), base=base), 2, n), total=n-2):
    n_digits += 1
    xs.append(n_coefficients)
    ys.append(n_digits)
print('√2 digits per coefficient:', n_digits / n_coefficients)
plt.plot(xs, ys, label='√2')

for _ in range(3):
    n_digits = 0
    n_coefficients = -1
    xs = []
    ys = []
    def digits():
        global n_digits
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
plt.xlabel('Continued Fraction Terms')
plt.ylabel('Decimal Digits')
plt.legend(loc='lower right')
plt.show()


# Khinchin's constant:
for n in (10, 100, 1000):
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

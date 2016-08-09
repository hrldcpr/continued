import sys

import continued


def coefficients():
    for line in sys.stdin:
        yield int(line)

for d in continued.as_digits(coefficients()):
    print(d, end='', flush=True)

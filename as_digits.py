import sys

import continued


def coefficients():
    for line in sys.stdin:
        yield int(line)

if sys.stdin.isatty():
    sys.stderr.write('Enter one coefficient per line.\n'
                     'Finish with Control-D:\n')
for d in continued.as_digits(coefficients()):
    print(d, end='', flush=True)

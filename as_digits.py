import sys

import continued


def coefficients():
    for line in sys.stdin:
        yield int(line)


if sys.stdin.isatty():
    pretty = sys.stdout.isatty()
    sys.stderr.write('Enter one coefficient per line.\n'
                     'Finish with Control-D:\n')
else: pretty = False

for d in continued.as_digits(coefficients()):
    if pretty: print('\t', d)
    else: print(d, end='', flush=True)

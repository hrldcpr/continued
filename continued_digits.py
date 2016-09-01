import sys

import continued


def digits():
    while True:
        c = sys.stdin.read(1)
        if not c: break
        try: yield int(c)
        except: yield c


if sys.stdin.isatty():
    pretty = sys.stdout.isatty()
    # TODO in this case, change digits() (and instructions) to do one per line
    sys.stderr.write('Enter digits followed by a decimal point followed by digits.\n'
                     'Use Control-D any time to flush the terminal input,\n'
                     'and Control-D Control-D to finish:\n')
else: pretty = False

for a in continued.continued_digits(digits()):
    if pretty: print('\t', a)
    else: print(a)

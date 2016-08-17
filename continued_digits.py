import sys

import continued


def digits():
    while True:
        c = sys.stdin.read(1)
        if not c: break
        try: yield int(c)
        except: yield c

if sys.stdin.isatty():
    sys.stderr.write('Enter digits followed by a decimal point followed by digits.\n'
                     'Use Control-D any time to flush the terminal input,\n'
                     'and Control-D Control-D to finish:\n')
for a in continued.continued_digits(digits()):
    print(a)

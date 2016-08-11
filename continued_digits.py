import sys

import continued


def digits():
    while True:
        c = sys.stdin.read(1)
        if not c: break
        try: yield int(c)
        except: yield c

for a in continued.continued_digits(digits()):
    print(a)

import continued


def coefficients():
    while True:
        yield 1

def digits():
    return continued.as_digits(coefficients())


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate infinite stream of golden ratio coefficients or digits.')
    parser.add_argument('--digits', action='store_true')
    args = parser.parse_args()

    if args.digits:
        for d in digits():
            print(d, end='', flush=True)

    else:
        for a in coefficients():
            print(a)

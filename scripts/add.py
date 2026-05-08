def add(a, b):
    return a + b


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python add.py <a> <b>")
        sys.exit(1)

    try:
        x = float(sys.argv[1])
        y = float(sys.argv[2])
    except ValueError:
        print("Error: arguments must be numbers")
        sys.exit(1)

    print(add(x, y))

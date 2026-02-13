import sys

if len(sys.argv) < 2:
    sys.exit("Too few command-line arguments")

if len(sys.argv) > 2:
    sys.exit("Too many command-line arguments")

filename = sys.argv[1]

if not filename.endswith(".py"):
    sys.exit("Not a Python file")

try:
    line_count = 0
    with open(filename) as file:
        for line in file:
            stripped = line.lstrip()
            if stripped and not stripped.startswith("#"):
                line_count += 1
    print(line_count)

except FileNotFoundError:
    sys.exit("File does not exist")

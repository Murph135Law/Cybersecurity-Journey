import csv
import sys
from tabulate import tabulate

if len(sys.argv) < 2:
    sys.exit("Too few command-line arguments")

if len(sys.argv) > 2:
    sys.exit("Too many command-line arguments")

filename = sys.argv[1]

if not filename.endswith(".csv"):
    sys.exit("Not a CSV file")

try:
    with open(filename) as file:
        reader = csv.reader(file)
        data = list(reader)
        print(tabulate(data[1:], headers=data[0], tablefmt="grid"))

except FileNotFoundError:
    sys.exit("File does not exist")

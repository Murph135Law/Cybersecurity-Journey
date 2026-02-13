import csv
import sys

if len(sys.argv) < 3:
    sys.exit("Too few command-line arguments")

if len(sys.argv) > 3:
    sys.exit("Too many command-line arguments")

before_file = sys.argv[1]
after_file = sys.argv[2]

try:
    with open(before_file) as input_file:
        reader = csv.DictReader(input_file)

        with open(after_file, "w") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=["first", "last", "house"])
            writer.writeheader()

            for row in reader:
                last, first = row["name"].split(", ")
                writer.writerow({"first": first, "last": last, "house": row["house"]})

except FileNotFoundError:
    sys.exit(f"Could not read {before_file}")

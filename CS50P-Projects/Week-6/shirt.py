from PIL import Image, ImageOps
import os
import sys


if len(sys.argv) < 3:
    sys.exit("Too few command-line arguments")

if len(sys.argv) > 3:
    sys.exit("Too many command-line arguments")

input = sys.argv[1]
output = sys.argv[2]

valid_extensions = [".jpeg", ".jpg", ".png"]

input_ext = os.path.splitext(input)[1]
output_ext = os.path.splitext(output)[1]

if input_ext not in valid_extensions or output_ext not in valid_extensions:
    sys.exit("Invalid input")

if input_ext != output_ext:
    sys.exit("Input and output have different extensions")

shirt = Image.open("shirt.png")

try:
    input_image = Image.open(input)

    size = shirt.size
    input_image = ImageOps.fit(input_image, size)

    input_image.paste(shirt, shirt)

    input_image.save(output)

except FileNotFoundError:
    sys.exit("Input does not exist")


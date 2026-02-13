""" first attempt
greeting = input("Greeting: ").strip().lower()
first_word = greeting[:5]
first_char = greeting[0]

if first_word == "hello":
    print("$0")
elif first_char == "h":
    print("$20")
else:
    print("$100")
"""

greeting = input("Greeting: ").strip().lower()

if greeting.startswith("hello"):
    print("$0")
elif greeting.startswith("h"):
    print("$20")
else:
    print("$100")

message = input("Input: ").strip()
vowels = ["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]
result = ""

for char in range(len(message)):
    if message[char] not in vowels:
        result += message[char]

print("Output:",result)

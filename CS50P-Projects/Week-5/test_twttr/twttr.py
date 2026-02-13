def main():
    str_input = input("Input: ").strip()

    shortened = shorten(str_input)

    print("Output:",shortened)

def shorten(word):
    vowels = ["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]
    result = ""

    for char in word:
        if char not in vowels:
            result += char

    return result

if __name__ == "__main__":
    main()

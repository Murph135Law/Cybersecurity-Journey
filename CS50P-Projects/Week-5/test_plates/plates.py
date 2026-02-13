def main():
    plate = input("Plate: ")
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")


def is_valid(s):
#Rule 1: length 2-6
    if not 2 <= len(s) <= 6:
        return False
#Rule 2: starts with 2 letters
    if not s[:2].isalpha():
        return False
#Rule 3: only letters and digits allowed
    if not s.isalnum():
        return False
#Rule 4: first number used cannot be "0"
    for c in s:
        if c.isdigit():
            if c == "0":
                return False
            break
#Rule 5: numbers only at the end (once a digit appear -> only digits after)
    seen_digit = False
    for c in s:
        if c.isdigit():
            seen_digit = True
        elif seen_digit:
            return False

    return True

if __name__ == "__main__":
    main()

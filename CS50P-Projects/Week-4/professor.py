import random


def main():
    n = get_level()

    score = 0
    for i in range(10):
        X = generate_integer(n)
        Y = generate_integer(n)

        attempt = 0
        for j in range(3):
            answer = input(f"{X} + {Y} = ")
            try:
                if int(answer) == X + Y:
                    score += 1
                    break

                else:
                    print("EEE")
                    attempt += 1
                    if attempt == 3:
                        print(X + Y)

            except ValueError:
                print("EEE")
                attempt += 1
                if attempt == 3:
                    print(X + Y)

    print(f"Score: {score}")


def get_level():
    while True:
        ui = input("Level: ")

        if ui not in ("1", "2", "3"):
            continue
        else:
            return ui


def generate_integer(level):
    level = int(level)

    if level not in (1, 2, 3):
        raise ValueError("")
    level = int(level)

    if level == 1:
        min_value = 0

    else:
        min_value = 10 ** (level - 1)
        
    max_value = (10 ** level) - 1
    integer = random.randint(min_value, max_value)
    return int(integer)


if __name__ == "__main__":
    main()

def main():
    user_input = input("camelCase: ").strip()
    result = convert(user_input)

    print("snake_case:",result)

def convert(arg_place_holder):
    snake = ""
    for char in arg_place_holder:
        if char.isupper():
            snake += "_" + char.lower()
        else:
            snake += char
    return snake.lstrip("_")


if __name__ == "__main__":
    main()

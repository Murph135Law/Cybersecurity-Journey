def main():
    while True:
        fraction = input("Fraction: ").strip()
        try:
            percentage = convert(fraction)
            output = gauge(percentage)
            print(output)
            break
        except (ValueError, ZeroDivisionError):
            pass


def convert(fraction):
    x_str, z_str = fraction.split("/")
    x = int(x_str)
    z = int(z_str)

    if z == 0:
        raise ZeroDivisionError
    if x < 0 or x > z:
        raise ValueError

    return round(x / z * 100)


def gauge(percentage):
    if percentage >= 99:
        return "F"
    elif percentage <= 1:
        return "E"
    else:
        return f"{percentage}%"


if __name__ == "__main__":
    main()

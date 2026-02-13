while True:
    fraction = input("Fraction: ").strip()

    try:
        x_str, z_str = fraction.split("/")

        x = int(x_str)
        z = int(z_str)

        if z == 0:
            print("Invalid input. Please enter a fraction like 1/2 or 3/4")
            continue
        if x < 0:
            print("Invalid input. Please enter a fraction like 1/2 or 3/4")
            continue
        if x > z:
            print("Invalid input. Please enter a fraction like 1/2 or 3/4")
            continue

        percentage = round(x / z * 100)

        if percentage >= 99:
            print("F")
        elif percentage <= 1:
            print("E")
        else:
            print(f"{percentage}%")
        break

    except (ValueError, ZeroDivisionError):
        print("Invalid input. Please enter a fraction like 1/2 or 3/4")

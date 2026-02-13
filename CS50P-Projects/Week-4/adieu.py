
names = []

try:
    while True:
        ui = input("Name: ").strip().title()
        names.append(ui)

except EOFError:
    if not names:
        print("\nAdieu, adieu, to nobody at all!")
    elif len(names) == 1:
        print(f"\nAdieu, adieu, to {names[0]}")
    elif len(names) == 2:
        print(f"\nAdieu, adieu, to {names[0]} and {names[1]}")
    else:
        main_part = ", ".join(names[:-1])
        print(f"\nAdieu, adieu, to {main_part}, and {names[-1]}")




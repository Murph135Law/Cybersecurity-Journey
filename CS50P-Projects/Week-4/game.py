from random import randrange

while True:
    try:
        ui = int(input("Level: "))
        if ui <= 0:
            continue

    except ValueError:
        continue

    n = randrange(int(ui))
    if n == 0:
        n += 1

    while True:
        try:
            guess = int(input("Guess: "))
            if guess <= 0:
                continue
            elif guess > n:
                print("Too large!")
            elif guess < n:
                print("Too small!")
            else:
                print("Just right!")
                break

        except ValueError:
            continue
    break

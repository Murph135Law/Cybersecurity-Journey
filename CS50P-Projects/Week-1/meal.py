def main():
    time = input("What time is it? ")
    converted = convert(time)

    if converted >= 7 and converted <= 8:
        print("Breakfast time")
    elif converted >= 12 and converted <= 13:
        print("Lunch time")
    elif converted >= 18 and converted <= 19:
        print("Dinner time")
    else:
        print()


def convert(time):
    hours, minutes = time.split(":")
    hours = float(hours)
    minutes = float(minutes) / 60
    return(hours + minutes)

if __name__ == "__main__":
    main()

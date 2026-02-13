def get_numeric(month_str):
    months = [
        {"name":"January", "numeric":"01"},
        {"name":"February","numeric":"02"},
        {"name":"March","numeric":"03"},
        {"name":"April","numeric":"04"},
        {"name":"May","numeric":"05"},
        {"name":"June","numeric":"06"},
        {"name":"July","numeric":"07"},
        {"name":"August","numeric":"08"},
        {"name":"September","numeric":"09"},
        {"name":"October","numeric":"10"},
        {"name":"November","numeric":"11"},
        {"name":"December","numeric":"12"},
    ]

    for month in months:
        if month["name"] == month_str:
            return int(month["numeric"])

    try:
        m = int(month_str)
        if 1 <= m <= 12:
            return m
        else:
            raise ValueError
    except ValueError:
        raise ValueError


def date_cleaned(date_input):
    date_input = date_input.replace("/", " ")
    date_input = date_input.replace(",","")
    return date_input


def convert_int(str):
    str = int(str)
    return str


def main():

    while True:
        try:
            date_input = input("Date: ").strip()

            if "/" in date_input:
                parts = date_input.split("/")
                if len(parts) != 3:
                    continue
                month_str, day_str, year_str = [p.strip() for p in parts]

                if not month_str.isdigit():
                    continue

            else:
                if "," not in date_input:
                    continue
                left, year_str = date_input.split(",", 1)
                year_str = year_str.strip()
                md_parts = left.split()
                if len(md_parts) != 2:
                    continue
                month_str, day_str = [p.strip() for p in md_parts]

            day = convert_int(day_str)
            year = convert_int(year_str)
            month = get_numeric(month_str)

            if day > 31 or day < 1:
                continue

            print(f"{year:04d}-{month:02d}-{day:02d}")
            break

        except ValueError:
            pass

        except EOFError:
            break


if __name__ == "__main__":
    main()

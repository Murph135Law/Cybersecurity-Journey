def load_menu():
    return [
        {"name": "Baja Taco", "price": "4.25"},
        {"name": "Burrito", "price": "7.50"},
        {"name": "Bowl", "price": "8.50"},
        {"name": "Nachos", "price": "11.00"},
        {"name": "Quesadilla", "price": "8.50"},
        {"name": "Super Burrito", "price": "8.50"},
        {"name": "Super Quesadilla", "price": "9.50"},
        {"name": "Taco", "price": "3.00"},
        {"name": "Tortilla Salad", "price": "8.00"},
]

def find_item_price(menu, item_name):

    for item in menu:
        if item["name"] == item_name:
            return item["price"]
    return None

def main():

    menu = load_menu()
    total = 0.0

    print("Please Choose From the Menu:")
    for item in menu:
        print(item["name"], f"${item["price"]}", sep="...." )

    while True:
        try:
            item_name = input("Item: ").title().strip()

            if not item_name:
                continue

            price = find_item_price(menu, item_name)

            if price is not None:
                total += float(price)
                print(f"Total: ${total:.2f}")
            else:
                pass

        except (EOFError, KeyboardInterrupt):
            break

if __name__ == "__main__":

    main()

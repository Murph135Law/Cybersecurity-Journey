from collections import Counter

groceries = []

while True:

    try:
        item = input().strip().upper()
        if item:
            groceries.append(item)

    except EOFError:
        break

if groceries:
    for item, count in sorted(Counter(groceries).items()):
        print(f"{count} {item}")

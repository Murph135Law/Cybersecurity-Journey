balance = 50

while balance > 0:
    print("Amount Due:", balance)
    coin = int(input("Insert Coin: "))

    if coin in (25, 10, 5):
        balance -= coin

print("Change Owed:", balance * -1)



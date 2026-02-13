import sys
import requests

if len(sys.argv) != 2:
    sys.exit("Missing command-line argument")

try:
    btc = float(sys.argv[1])

except ValueError:
    sys.exit("Command-line argument is not a number")

try:
    response = requests.get("https://rest.coincap.io/v3/assets/bitcoin?apiKey=d25b56c0956ff58159984f938c41e9f5c778a3be432db26d532ff5397b058035")
    data = response.json()
    
    price = float(data["data"]["priceUsd"])
    result = btc * price

    print(f"${result:,.4f}")

except requests.RequestException:
    sys.exit("Error fetching Bitcoin price")


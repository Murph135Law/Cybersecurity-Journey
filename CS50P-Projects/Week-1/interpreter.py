expression = input("Expression: ").strip()

x, operator, z = expression.split()

x = float(x)
z = float(z)

if operator == "+":
    result = x + z
elif operator == "-":
    result = x - z
elif operator == "*":
    result = x * z
elif operator == "/":
    result = x / z
else:
    print("Unsupported operator!")


print(result)

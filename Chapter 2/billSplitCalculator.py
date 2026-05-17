# Write a program that takes total bill amount and number of friends as input.
# Calculate how much each person will pay.
# Also print the data type of each variable used.
x = float(input("Total bill: "))
y = int(input("Friends: "))
z = x/y
print("Each will pay: ", z)
print("Data type of Total bill: ", type(x))
print("Data type of Friends: ", type(y))
print("Data type of Split amount: ", type(z))

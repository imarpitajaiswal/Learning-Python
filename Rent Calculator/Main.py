# Inputs we need from the user
# 1. Total rent
# 2. Total food ordered for snacking
# 3. Electricity units consumed
# 4. Charge for electricity per unit
# 5. Number of roomates sharing the rent and food expenses (optional, if you want to split the bill)

# Output:
# Total amount you have to pay at the end of the month is: xyz

rent = int(input("Enter the total rent: "))
food = int(input("Enter the total food ordered for snacking: "))
electricity_units = int(input("Enter the electricity units consumed: "))
charge_per_unit = int(input("Enter the charge for electricity per unit: "))
roommates = int(input("Enter the number of roomates: "))

total_electricity_charge = electricity_units * charge_per_unit
total_amount = (rent + food + total_electricity_charge)//roommates

if roommates > 0:
    total_amount /= roommates

print("Total amount you have to pay at the end of the month is: ", total_amount)
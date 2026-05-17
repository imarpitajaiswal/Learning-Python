# Create a program that asks the user for 5 favourite foods and prints them one by one
print("Question-4")
food1 = input("Enter your first favourite food: ")
food2 = input("Enter your second favourite food: ")
food3 = input("Enter your thirdfavourite food: ")
food4 = input("Enter your fourth favourite food: ")
food5 = input("Enter your fifth favourite food: ")
food = [food1,food2,food3,food4,food5]
for item in food:
    print(item)

print("Other way: ")

food_list=[]
for m in range(5):
    food=input(f"Enter your favourite food item {m+1}: ")
    food_list.append(food)
print("Your favourite food items are:")
for food in food_list:
    print(food)
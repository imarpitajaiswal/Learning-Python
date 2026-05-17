# Ask the user for their 3 favourite movies and store them in a list
a = input("Enter your favourite movie 1: ")
b = input("Enter your favourite movie 2: ")
c = input("Enter your favourite movie 3: ")
list1 = [a,b,c]
print(list1)

# Create a tuple of marks(87,64,33,95,76) and print the highest and lowest marks using max() and min()
tuple1 = (87,64,33,95,76)
print("Here's the tuple: ", tuple1)
print("maximum:", max(tuple1))
print("minimum: ", min(tuple1))

# Write a program to check grade based on marks (A/B/C/D) using if-elif-else
a = int(input("Entder your marks to get your grade: "))
if (a >= 90):
    print("Your grade is A")
elif (a >= 80):
    print("Your grade is B")
elif (a >= 70):
    print("Your grade is C")
else:
    print("Your grade is D")
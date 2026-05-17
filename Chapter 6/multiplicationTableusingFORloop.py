#Wite a program that prints the multiplication table of any number entered by the user using a for loop
print("QUESTION 4")
j = int(input("Enter a number:"))
for i in range(1,11):
    print(f"{j} * {i} = {j*i}")
    i+=1
# Take diameter as input and calculate area of a circle
print("Program to calculae area of circle using diameter given by the user")
d = float(input("Enter the diamenter of the Circle: "))
r = d / 2
# area = 3.14*r*r
area = 3.14 *(r**2)
print("Area of the Circle is : ", area)
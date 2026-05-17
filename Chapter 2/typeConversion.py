# Take a number as input, convert it to a float, 
# print both the original and the converted values with their data types.
print("Explicit Conversion:")
num = int(input("Enter your number: "))
print("Original number is: ", num)
print("Original data type is: ", type(num))
num1 = float(num)
print("Converted number is: ", num1)
print("Converted data type is: ", type(num1))
# Take input in Celcius and print its equivalent in Fahrenheit and Kelvin
# (Use explicit type conversion and arithmetic operators.)
# Formula:
#      Fahrenheit = (C*9/5)+32
#      Kelvin = C + 273.15
c = float(input("Enter your temperature in Celcius: "))
f = (c*(9/5))+32
k = c + 273.15
print("Given temperature in Fahrenheit is: ", f)
print("Given temperature in Kelvin is: ", k)
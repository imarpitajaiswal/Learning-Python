# Write a program that:
#       takes a sentence as input
#       converts it to lowercase
#       replaces all spaces" " with underscores"_"
#       prints the new string
str = input("Enter your sentence: ")
print(str.lower())
str1 = str.replace(" ", "_")
print(str1)
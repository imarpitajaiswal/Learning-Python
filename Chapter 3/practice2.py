# Write a program to take input from user
# print middle 3 characters and last 2 characters
str1 = input("Enter your word: ")
mid = len(str1)//2
print(str1[mid-1:mid+2])
print(str1[-2:])
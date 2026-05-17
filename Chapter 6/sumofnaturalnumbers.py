# Write a program to find sum of n natural numbers
# For eg- if n=5, then output is 1+2+3+4+5=15
# Hint: Keep a running total inside the loop
i = int(input("Enter the value of n to find the sum: "))
sum = 0
while (i>=1):
    sum=sum+i
    i = i-1
print("Total: ", sum)
print("Let's try the same with another code:")
n = int(input("Enter a number: "))
sum1=0
count=1
while (count<=n):
    sum1=sum1+count
    count+=1
print("Total sum is: ", sum1)
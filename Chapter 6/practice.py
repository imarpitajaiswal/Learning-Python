# print numbers from 1 to 100 using a for loop
for i in range(1,101,1):
    print(i)

# print numbers from 100 to 1 using a while loop
print("Question-2")
j=100
while j>=1:
    print(j)
    j-=1

# print all numbers from 1 to 50 except multiples of 5 
print("Question-3")
for k in range(1,51,1):
    if k%5==0:
        continue
    print(k)

# print sum of first 10 natural numbers using while loop
l=1
sum=0
while l<=10:
    sum=sum+l
    l+=1
print(sum)  
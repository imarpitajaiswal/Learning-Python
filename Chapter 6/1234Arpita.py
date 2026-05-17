#Wite a program to print numbers from 1 to 50, but print "Arpita Jaiswal" instead of numbers that are multiples of 5
# eg- 1234 Arpita Jaiswal 6789 Arpita Jaiswal
print("QUESTION 2")
for i in range(1,51):
    if i%5==0:
        print("Arpita Jaiswal")
    else:
        print(i)
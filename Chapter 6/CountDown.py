#Print a countdown before something "exciting" happens (like "Launching", "Happy New Year!")
import time
count =int(input("Enter the Coundown: "))
print("\n Count Down Starts Now!!")
for i in range(count,0,-1):
    print(i)
    time.sleep(1)
print("\n WOHOO! Happy New Year!!")

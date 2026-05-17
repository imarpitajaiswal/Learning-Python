# write a program to read a text from a given file certificate.text 
# and find wheather it contains the word live

file = open("certificate.txt", "r")
data = file.read()
data = data.lower()
if "live" in data:
    print("Yes, live is present in the file.")
else:
    print("No, live is not in the file.")
file.close()

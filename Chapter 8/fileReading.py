file = open("file1.txt", "a")
file.write("\nAll Set!!")
file.close()

with open("certificate.txt","r") as f:
    data = f.read()
    print("File the data",data)
    
file = open("file2.txt","x")
file.write()
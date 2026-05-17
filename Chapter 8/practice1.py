import shutil
shutil.copy("notes.txt","notes_backup.txt")
import os
os.rename("temp.txt","final.txt")

# get file name from user and save in a backup folder

# file1 = input("Enter your file name: ")
# data = file1.write("file")
# os.rename("file1.txt")
try:
    with open("notes.txt","r") as f:
        tempt = f.readline()
        print(len(notes.txt))

except:
    print("invalid file name")
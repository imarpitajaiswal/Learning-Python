#methods of list
marks = [99,100,90,99,95]
print("Given list: ", marks)
print("maximum marks is:", max(marks))
marks.append(92)
print("Added new number:", marks)
marks[1] = 98
print("chenged 2nd number:", marks)
marks.sort()
print("Sorted list: ", marks)
marks.pop(0)
print("Popped 1st number:", marks)
marks.insert(1,98)
print("New number added: ", marks)
mid = (len(marks)//2)
print("Middle 2 numbers:", marks[mid-1:mid+1])
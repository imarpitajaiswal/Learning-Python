# You are given a list of programming languages:
# ["Python", "Java","C++", "Python", "Java","C"]
# Convert it into a set and print how many unique languages Divya knows
list1 = ["Python", "Java","C++", "Python", "Java","C"]
# covert list into set
list1 = set(list1)
print(list1)
print(type(list1))
print("Divya knows", len(list1), "unique languages.")
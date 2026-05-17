# Dictionary Basics
student = {
    "name" : "Aditya",
    "city" : "Delhi",
    "age" : 25,
    "roll" : 567,
    "name" : "Arpita"
}
print(type(student))
print(student)
print(student['name'])
student["city"] = "Paris"
print(student)
student["favSubject"]="Maths"
print(student)
student.pop("favSubject")
print(student.keys())
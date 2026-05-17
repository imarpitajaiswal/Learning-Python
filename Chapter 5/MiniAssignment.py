# Create a dictionary storing meanings of 3 english words.

dict1 = {
    "Obfuscate" : "To make something unclear or confusing.",
    "Pernicious" : "Harmful in a gradual or subtle way.",
    "Quixotic" : "Extremely idealistic, impractical, or unrealistic."
}
print(dict1)
print(type(dict1))
dict1["Serendipity"] = "the occurance of events by chance in a happy or beneficial way"
print("updated dictionary is: ", dict1)

dict2 = {
    "ram" : "sita",
    "krishna" : "radha",
    "shiv" : "parvati"
}
print(dict2)
dict2["narayan"] = "laxmi"
print("updated dictionary is:", dict2)

# Create a set of numbers and show union and intersection with another set.
set1 = {"sita", "ram", "laxmi", "narayan", "parvati", "shiv"}
set2 = {"hari", "radha", "krishna", "laxmi", "narayan"}
print(type(set1))
union_set = set1.union(set2)
print("Union: ", union_set)
int_set = set1.intersection(set2)
print("Intersection: ", int_set)


# write a funtion that takes a string and returns the count of vowels and consonants separately

def countVowConso(userInput):
    vowels ="aeiouAEIOU"

    countVow = 0
    countConso = 0

    for each in userInput:
        if each.isalpha():
            if each in vowels:
                countVow+=1
            else:
                countConso+=1
    
    return countVow,countConso

vowels,consonants = countVowConso("Arpita Jaiswal")
print(vowels,consonants)

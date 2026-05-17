# Convert text-based emotions into emojis.
str = input("Enter your message: ")
str = (str.replace(":)", "🙂"))
str = (str.replace(":(", "🙁"))
str = (str.replace(":[", "😬"))
str = (str.replace(";)", "😉"))
print(str)
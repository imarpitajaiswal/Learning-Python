# Designed a smart chatbot using Python fundamentals (loop, conditions, and dictionaries). 
# Implemented a keyboard-matching logic to make it behave like a real AI Assistant and built modular functions for reuseability.
# (Future plan: connect to OpenAI API for real AI responses.)
# With time based personalised greeting! Responses after 1 second time delay

import datetime
import time

name = input("Namaste! Please enter your good name: ")
presentHour = datetime.datetime.now().hour

if 5<= presentHour <= 11:
    print("Good Morning ", name)
elif 11<= presentHour <= 17:
    print("Good Afternoon ", name)
elif 17<= presentHour <= 20:
    print("Good Evening ", name)
else:
    print("Good Night", name)

print("Namaste!! Welcome to your AI Chatbot.")
print('''You can ask me a question.''')
print('''Type "Bye" if you want to exit.''')

responses = {
    "hello": "Hi! Welcome, How are you?",
    "how are you": "I am Great. Thanks for asking.",
    "who are you": "I am your smart AI Chatbot.",
    "motivate me": "Keep coding! Every bug in your project makes you a better developer.",
    "happy": "Great to hear that.",
    "what are functions": "Go to Chapter 7"
}

def botResponses(userInput):
    userInput = userInput.lower()
    for each in responses:
        if each in userInput:
            time.sleep(1)
            return responses[each]
            
    return "I am unable to answer. I am still learning."

while True:
    userInput = input("Ask me a question: ")
    result = botResponses(userInput)
    print("Bot Response: ", result)
    
    if "bye" in userInput.lower():
        print("Thank you for using AI Smart Bot.")
        break
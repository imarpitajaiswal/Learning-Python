# Create a console-based Expense trcker program in Python that allows the usert to record daily expenses and view summaries 
# like total spending. 
# Use only the concepts learned till Chapter 6(loops,conditions,lists,dictionaries, and basic input/output).
'''
You are required to build a simple personal finance management tool. The program should allow the user to:
    Add an expense with details like data, category, description, and amount.
    View all recorded expenses in a clean format.
    Exit the program gracefully when the user choses to.
All tasks must be implemented using loops, if-else, lists, and dictionaries only. No user-defined functions should be used.
'''

expenses=[]
print("Welcome to Personal Finance Management Tool 🙏🏻")

while True:
    print("==========MENU=============")
    print("Choose 1 : To add Expenses ")
    print("Choose 2 : To view all Expenses ")
    print("Choose 3 : To view total Expenses ")
    print("Choose 4 : EXIT ")

    choice = int(input("Enter your choice: "))

# To add Expenses
    if (choice == 1):
        date = input("Enter date of expense: ")
        category = input("Enter category of expense: ")
        description = input("Enter description of expense: ")
        amount = float(input("Enter amount of expense: "))

        expense ={
            "Date" : date,
            "Category" : category,
            "Description" : description,
            "Amount" : amount
        }
        expenses.append(expense)
        print("\n Your expense is added Successfully! ")

# To view all expenses
    elif (choice == 2):
        if (len(expenses)==0):
            print("First add an expense to view.")
        else:
            print("====Following are your expenses====")
            count = 1
            for item in expenses:
                print(f"Expense{count} -> {item["Date"]}, {item["Category"]}, {item["Description"]}, {item["Amount"]}")
                count+=1

# To view total expenses
    elif (choice == 3):
        total=0
        for item in expenses:
            total = total + item["Amount"]
        print("\n Your total expense is: ", total)


# To EXIT
    elif (choice ==4):
        print("\n Thank you for your time. ")
        break

    else:
        print("\n INVALID INPUT!! TRY AGAIN.")
#### Coders: Logan Galowitsch and William Finck 
#### Goal: create menu for interacting with database
#### Date: 2/18/2024
#### Code below uses sample code from Susan Gauch

import os.path
from Database import DB

Titanic = DB()

# Menu Function
def menu():
    print("Welcome to the Database")
    print()

    done = False
    while done == False:
        choice = input("""
        1) Create new database
        2) Open database
        3) Close database
        4) Read record
        5) Display record
        6) Update record
        7) Create report
        8) Delete record
        9) Add record
        10) Quit

        Please enter your choice: """)

        choice = int(choice)
        if choice == 1:
           #infinite loop till the user types a valid csv file
           while True:
              created_db_file = input("What is the name of the file? ")
              if not os.path.isfile(created_db_file + str(".csv")):
                 print(str(created_db_file)+".csv not found")
              else:
                 Titanic.createDB(created_db_file)
                 break

        elif choice == 2:
           #Checks to see if a database is already open. If not, prompts the user with the available databases to open.
           if Titanic.isOpen():
              print("A database is already open. Please close that first.")
           else:
              selected_database = input("Type the database you want to open: ")
              Titanic.OpenDB(selected_database)

        elif choice == 3:
           #Closes the database
           Titanic.CloseDB()

        elif choice == 4:
           #Get specific record by seeking to that place. If no database is open, print error message.
           if Titanic.isOpen():
              number = input("What record do you want to read? ")
              Titanic.getRecord(int(number))
              print("Record "+ str(number) + ", ID: "+Titanic.record["ID"]+"\t first_name: "+Titanic.record["first_name"]+"\t last_name: "+Titanic.record["last_name"]+"\t age: "+str(Titanic.record["age"])+"\t ticket_num: "+Titanic.record["ticket_num"]+"\t fare: "+Titanic.record["fare"]+"\t date_of_purchase: "+Titanic.record["date_of_purchase"])
           else:
              print("Database is closed. Open to use.")

        elif choice == 5:
           passengerId = input("Please input the Passenger ID you wish to display: ")
           Titanic.displayRecord(passengerId)

        elif choice == 6:
           passengerId = input("Enter the Passenger ID to update the record: ")
           Titanic.updateRecord(passengerId)
        elif choice == 7:
            if Titanic.isOpen():
              print("Creating report:")
              for i in range(10):
                 Titanic.getRecord(i)
                 print(f"Record {i}: {Titanic.record}")
            else:
               print("Database is closed. Open to use")
        
        elif choice == 8:
           passengerId = input("Enter the Passenger ID to delete the record: ")
           Titanic.deleteRecord(passengerId)
           
        elif choice == 9:
           if Titanic.isOpen():
                # Collect data for the new record
                passengerId = input("Enter Passenger ID: ")
                fname = input("Enter first name: ")
                lname = input("Enter last name: ")
                age = input("Enter age: ")
                ticketNum = input("Enter ticket number: ")
                fare = input("Enter fare: ")
                date = input("Enter date of purchase: ")

                Titanic.addRecord(passengerId, fname, lname, age, ticketNum, fare, date)
            
        elif choice == 10:
           if Titanic.isOpen():
              print ("Please close the database first.")
           else:
              print("Quitting")
              done = True
        else:
           print("Invalid option")


# Calling the Menu Function
menu()
from Database import DB

filepath = None
DBsize = 20
rec_size = 72

Titanic = DB()
#sample.creatSB(filepath)
while True:
    print('Database Menu')
    print('--------------')
    print('1. Create new DB')
    print('2. Open DB')
    print('3. Close DB')
    print('4. Read Record')
    print('5. Display Record')
    print('6. Create Report')
    print('7. Update Record')
    print('8. Delete Record')
    print('9. Add Record')
    print('\n')
    key = input('Please select an option 1-9: ').strip()
    if key == '1':
        #Create new DB
        filepath = input("Please input the name of the csv file you wish to create a DB with: ")
        Titanic.createDB(filepath)
        continue
    elif key == '2':
        #Open DB
        openDB = input("Please input the name of the file you wish to open a DB with: ")
        Titanic.open(openDB)
        print("The database has been opened\n")
        continue
    elif key == '3':
        #Close DB
        Titanic.close()
        continue
    elif key == '4':
        #Read Record
        
        continue
    elif key == '5':
        #Display Record
        
        continue
    elif key == '6':
        #Create Report
        
        continue
    elif key == '7':
        #Update Record
        
        continue
    elif key == '8':
        #Delete Record
        cin = input("Please indicate the ID of the record you wish to remove: ")
        Titanic.deleteRecord(cin)
        continue
    elif key == '9':
        #Add Record
        Titanic.addRecord()
    else:
        print('wrong input please try again')
        continue


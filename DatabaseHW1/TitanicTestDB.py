from Database import DB

filepath = "SmallTitanic"
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
    print('4. Display Record')
    print('5. Update Record')
    print('6. Create Report')
    print('7. Add Record')
    print('8. Delete Record')
    print('9. Quit')
    print('\n')
    key = input('Please select an option 1-9: ').strip()
    if key == '1':
        #Create new DB
        Titanic.createDB('SmallTitanic')
        continue
    elif key == '2':
        #Open DB
        Titanic.open('SmallTitanic')
        continue
    elif key == '3':
        #Close DB
        Titanic.close()
        continue
    elif key == '4':
        #Display Record
        continue
    elif key == '5':
        #Update Record
        continue
    elif key == '6':
        #Create Report
        continue
    elif key == '7':
        #Add Record
        continue
    elif key == '8':
        #Delete Record
        continue
    elif key == '9':
        #Quit
        Titanic.CloseDB()
        break
    else:
        print('wrong input please try again')
        continue


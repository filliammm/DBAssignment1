from Database import DB

filepath = "SmallTitanic"
DBsize = 20
rec_size = 72

sample= DB()
#sample.creatSB(filepath)
while True:
    print('Database Menu')
    print('--------------')
    print('1. ReadCSV')
    print('2. writeRecord')
    print('3. CreateDB')
    print('4. Open')
    print('5. readRecord')
    print('\n')
    key = input('Please select an option 1-5: ').strip()
    if key == '1':
        #ReadCSV
        break
    elif key == '2':
        #Wrtite Record
        break
    elif key == '3':
        #CreateDB
        break
    elif key == '4':
        #Open
        break
    elif key == '5':
        #read record
        break
    else:
        print('wrong input please try again')
        continue


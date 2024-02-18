#-----------------------------
# HW1 Part 1 solution by Ananya Vangoor and Susan Gauch
#-----------------------------

import csv
import os.path

class DB:

    #default constructor
    def __init__(self):
        self.filestream = None
        self.num_records = 0
        self.record_size = 0
        self.fileptr = None

    #create database
    def createDB(self,filename):
        #Generate file names
        csv_filename = filename + ".csv"
        text_filename = filename + ".data"
        config_filename = filename + ".config"
        
        # Read the CSV file and write into data files
        with open(csv_filename, "r") as csv_file:
            data_list = list(csv.DictReader(csv_file,fieldnames=('ID','first_name','last_name','age','ticket_num', 'fare', 'date_of_purchase')))

        
		# Formatting files with spaces so each field is fixed length, i.e. ID field has a fixed length of 86
        def writeDB(filestream, dict):
            filestream.write("{:5.5}".format(dict["ID"]))
            filestream.write("{:15.15}".format(dict["first_name"]))
            filestream.write("{:20.20}".format(dict["last_name"]))
            filestream.write("{:5.5}".format(dict["age"]))
            filestream.write("{:20.20}".format(dict["ticket_num"]))
            filestream.write("{:5.5}".format(dict["fare"]))
            filestream.write("{:15.15}".format(dict["date_of_purchase"]))
            filestream.write("\n")

        count = 0
        with open(text_filename,"w") as outfile:
            for dict in data_list:
                writeDB(outfile,dict)
                emptyRecord = {"ID": "0", "first_name": "Null", "last_name": "Null", "age": "0", "ticket_num": "0", "fare": "0", "date_of_purchase": "Null"}
                writeDB(outfile, emptyRecord)
                count += 2

        # Opening a config file for writing details
        self.num_records = count
        self.record_size = 86
        config_fileptr = open(config_filename, "w")
        config_fileptr.write(str(self.num_records) + "\n")
        config_fileptr.write(str(self.record_size) + "\n")
        config_fileptr.close()

    #seeking to a specific record method
    def getRecord(self, recordNum):
        self.flag = False
        ID = first_name = last_name = age = ticket_num = fare = date_of_purchase = "None"

        if 0 <= recordNum < self.num_records:
            self.fileptr.seek(0, 0)
            self.fileptr.seek(recordNum * self.record_size)
            line = self.fileptr.readline().rstrip('\n')
            self.flag = True
        else:
            print("You are going out of bounds. You will see an empty record. Choose something between 0 and", self.num_records - 1)
            self.flag = False
            self.record = dict({"ID": "0", "first_name": "Null", "last_name": "Null", "age": "0", "ticket_num": "0", "fare": "0", "date_of_purchase": "Null"})
            return -1, self.record

        if self.flag:
            ID = line[0:5]
            first_name = line[5:20]
            last_name = line[20:40]
            age = line[40:45]
            ticket_num = line[45:65]
            fare = line[65:70]
            date_of_purchase = line[70:85]
            self.record = dict({"ID": ID, "first_name": first_name, "last_name": last_name, "age": age,
                                "ticket_num": ticket_num, "fare": fare, "date_of_purchase": date_of_purchase})
            return 1, self.record
        else:
            return -1, None



     #Binary Search by record id
    def binarySearch(self, input_ID):
        low = 0
        high = self.num_records - 1
        found = False
        recordNum = None  # Initialize the insertion point

        while not found and high >= low:
            middle = (low + high) // 2
            self.getRecord(middle)
            mid_id = self.record["ID"]

            if mid_id.strip() == '_empty_':
                non_empty_record = self.findNearestNonEmpty(middle, low, high)
                if non_empty_record == -1:
                    # If no non-empty record found, set recordNum for potential insertion
                    recordNum = high
                    print("Could not find record with ID..", input_ID)
                    return False, recordNum

                middle = non_empty_record
                self.getRecord(middle)
                mid_id = self.record["ID"]
                if int(mid_id) > int(input_ID):
                    recordNum = middle - 1
                else:
                    recordNum = middle + 1

            if mid_id != '_empty_':
                try:
                    if int(mid_id) == int(input_ID):
                        found = True
                        recordNum = middle
                    elif int(mid_id) > int(input_ID):
                        high = middle - 1
                    elif int(mid_id) < int(input_ID):
                        low = middle + 1
                except ValueError:
                    # Handle non-integer IDs
                    high = middle - 1

        if not found and recordNum is None:
            # Set recordNum to high + 1 if no suitable spot is found
            recordNum = high
            print("Could not find record with ID", input_ID)

        return found, recordNum


    def findNearestNonEmpty(self, start, low_limit, high_limit):
        step = 1  # Initialize step size

        while True:
            # Check backward
            if start - step >= low_limit:
                self.getRecord(start - step)
                if self.record["ID"].strip() != "\0":
                    #print(self.record)
                    return start - step

            # Check forward
            if start + step <= high_limit:
                self.getRecord(start + step)
                if self.record["ID"].strip() != "\0":
                    #print(self.record)
                    return start + step

            # Increase step size and repeat
            step += 1

            # Terminate if beyond the search range
            if start - step < low_limit and start + step > high_limit:
                break

        return -1  # No non-empty record found


    #open the database/also acting as my read data method
    def OpenDB(self, nameDB):
        if self.isOpen():
           print("You already have a database open.  Please close it first.")
        else:
           data_file = nameDB + ".data"
           config_file = nameDB + ".config"
        
           if not os.path.isfile(data_file):
              print(str(data_file)+" not found")
           else:
              if not os.path.isfile(config_file):
                 print(str(config_file)+" not found")
              else:
                 self.fileptr = open(data_file, "r+")
                 config_fileptr = open (config_file, "r")
                 self.num_records = int(config_fileptr.readline())
                 self.record_size = int(config_fileptr.readline())
                 config_fileptr.close();

    #check if a database is already open or not
    def isOpen(self):
        if self.fileptr == None:
            return False
        else:
            return True


    #write Record method           
    def writeRecord(self, recordNum, passengerId, fname, lname, age, ticketNum, fare, date):
        # Implement writeRecord method to write a record to the data file
        if self.fileptr is not None:
            if 0 <= recordNum < self.num_records:
                # Move the file pointer to the beginning of the record
                self.fileptr.seek(recordNum * self.record_size)

                # Check if the record is empty
                if passengerId == '\0':
                    # Empty record
                    record_data = ''
                else:
                    # Format the record data (assuming a fixed format)
                    record_data = f"{passengerId},{fname},{lname},{age},{ticketNum},{fare},{date}"

                # Pad the record data if needed to match recordSize
                record_data = record_data.ljust(self.record_size, ' ')

                # Write the record to the file
                self.fileptr.write(record_data)

                print(f"Record {recordNum} updated successfully.")
                return 1  # 1 indicates successful update
            else:
                print("Invalid record number.")
                return -1  # -1 indicates an invalid record number


    def displayRecord(self, passengerId):
        found, recordNum = self.binarySearch(passengerId)

        if found:
            result, record = self.getRecord(recordNum)
            if result == 1:
                if record["ID"] != "_empty_":
                    # Display each field name and its corresponding value
                    for field_name, field_value in record.items():
                        print(f"{field_name}: {field_value}")
                else:
                    print(f"Record {recordNum} is empty.")
            else:
                print("Invalid record number or the database has not been open")
        else:
            print(f"Record with Passenger ID {passengerId} not found.")




    #update Record method        
    def updateRecord(self, passengerId):
        if self.isOpen():
            found, recordNum = self.binarySearch(passengerId)

            if found:
                # Get the existing record
                result, existing_record = self.getRecord(recordNum)

                if result == 1:
                    print("Existing record:")
                    self.displayRecord(passengerId)

                    # Get the new fare value from the user with input validation
                    while True:
                        new_fare = input("Enter new fare: ")
                        if new_fare.isdigit():  # Add more validation as needed
                            break
                        else:
                            print("Invalid input. Please enter a valid fare value.")

                    # Update the record with the new fare value
                    success = self.writeRecord(recordNum, passengerId, existing_record["first_name"],
                                                existing_record["last_name"], existing_record["age"],
                                                existing_record["ticket_num"], new_fare,
                                                existing_record["date_of_purchase"])

                    if success == 1:
                        print(f"Record with Passenger ID {passengerId} updated successfully.")
                    else:
                        print(f"Failed to update record with Passenger ID {passengerId}.")
                else:
                    print("Invalid record number or the database has not been open.")
            else:
                print(f"Record with Passenger ID {passengerId} not found.")





    #add Record method
    def addRecord(self, passengerId, fname, lname, age, ticketNum, fare, date):
        # Implement addRecord method
        if self.isOpen():
            # Search for an empty record
            recordNum, _, _, _, _, _, _, _ = self.binarySearch('\0')
            if recordNum != -1:
                # Call writeRecord to add the new record to an empty slot
                return self.writeRecord(recordNum, passengerId, fname, lname, age, ticketNum, fare, date)
            else:
                print("No empty record found. Trying to extend the file.")
                # You can implement the logic to extend the file and add the new record here
                # ...


    #delete Record method
    def deleteRecord(self, passengerId):
        # Implement deleteRecord method
        if self.isOpen():
            recordNum, _, _, _, _, _, _, _ = self.binarySearch(passengerId)
            if recordNum != -1:
                # Call writeRecord to delete the record by overwriting with default values
                return self.writeRecord(recordNum, '\0', '', '', '', '', '', '')
            else:
                print(f"Record with Passenger ID {passengerId} not found.")
                return False
    
    

    #close the database
    def CloseDB(self):
        if self.fileptr:
            self.fileptr.close()
            self.num_records = 0
            self.record_size = 0
            self.fileptr = None
            self.filestream = None
            print("Database closed!")
        else:
            print("You do not have any databases open to close them.")

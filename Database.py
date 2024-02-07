import csv
import os.path

class DB:

    #default constructor
    def __init__(self):
        self.filestream = None
        self.rec_size = 0
        self.num_record = 0
        self.Id_size= 10
        self.Fname_size= 30
        self.Lname_size= 30
        self.Age_size= 10
        self.Tnum_size= 20
        self.Fare_size = 10
        self.Date_size = 20


    #create database
    def createDB(self, filename):
    # Generate file names
        csv_filename = filename + ".csv"
        text_filename = filename + ".data"
        config_filename = filename + ".config"

        # Read the CSV file and write into data files
        with open(csv_filename, "r") as csv_file:
            data_list = list(csv.DictReader(csv_file, fieldnames=('ID', 'fname', 'lname', 'age', 'ticketnum', 'fare', 'date')))

        # Formatting files with spaces so each field is fixed length, i.e., ID field has a fixed length of 10
        def writeDB(filestream, dict):
            filestream.write("{:{width}.{width}}".format(dict["ID"], width=self.Id_size))
            filestream.write("{:{width}.{width}}".format(dict["fname"], width=self.Fname_size))
            filestream.write("{:{width}.{width}}".format(dict["lname"], width=self.Lname_size))
            filestream.write("{:{width}.{width}}".format(dict["age"], width=self.Age_size))
            filestream.write("{:{width}.{width}}".format(dict["ticketnum"], width=self.Tnum_size))
            filestream.write("{:{width}.{width}}".format(dict["fare"], width=self.Fare_size))
            filestream.write("{:{width}.{width}}".format(dict["date"], width=self.Date_size))
            filestream.write("\n")

            # write an empty record
            filestream.write("{:{width}.{width}}".format('_empty_', width=self.Id_size))
            filestream.write("{:{width}.{width}}".format(' ', width=self.Fname_size))
            filestream.write("{:{width}.{width}}".format(' ', width=self.Lname_size))
            filestream.write("{:{width}.{width}}".format(' ', width=self.Age_size))
            filestream.write("{:{width}.{width}}".format(' ', width=self.Tnum_size))
            filestream.write("{:{width}.{width}}".format(' ', width=self.Fare_size))
            filestream.write("{:{width}.{width}}".format(' ', width=self.Date_size))
            filestream.write("\n")

        with open(config_filename, "w") as config_file:
            config_file.write("20")
            self.rec_size = sum([self.Id_size, self.Fname_size, self.Lname_size, self.Age_size, self.Tnum_size, self.Fare_size, self.Date_size])
            config_file.write("72")

        with open(text_filename, "w") as outfile:
            for dict in data_list:
                writeDB(outfile, dict)

    #read the database
    def readDB(self, filename, DBsize, rec_size):
        self.filestream = filename + ".data"
        self.record_size = DBsize
        self.rec_size = rec_size
        
        if not os.path.isfile(self.filestream):
            print(str(self.filestream)+" not found")
        else:
            self.text_filename = open(self.filestream, 'r+')

    #read record method
    def getRecord(self, recordNum):

        self.flag = False
        id = fname = lname = age = ticketnum = fare = date = "None"

        if recordNum >=0 and recordNum < self.record_size:
            self.text_filename.seek(0,0)
            self.text_filename.seek(recordNum*self.rec_size)
            line= self.text_filename.readline().rstrip('\n')
            self.flag = True
        
        if self.flag:
            id = line[0:10]
            fname = line[10:40]
            lname = line[40:700]
            age = line[70:80]
            ticketnum = line[80:100]
            fare = line[100:110]
            date = line[110:130]
            self.record = dict({"ID": id, "fname": fname, "lname": lname, "age": age, "ticketnum": ticketnum, "fare": fare, "date": date})
    
    #open record function
    def open(self, db_name):
        # Implement open method to read config file and open data file
        config_filename = db_name + ".config"
        data_filename = db_name + ".data"
        try:
            with open(config_filename, 'r') as config_file:
                self.num_record = config_file.read()
                self.recordSize = config_file.read()

            self.filestream = open(data_filename, 'r+')
            return True
        except FileNotFoundError:
            return False
    #is open record method
    def isOpen(self):
        # Check if the database is open
        return self.filestream is not None
    
    #close record method
    def close(self):
        # Implement close method to close data file
        if self.filestream is not None:
            self.filestream.close()
            self.num_record = 0
            self.recordSize = 0
            self.filestream = None
    
    #display record method        
    def readRecord(self, recordNum, passengerId, fname, lname, age, ticketNum, fare, date):
        # Implement readRecord method to read a record from the data file
        if self.isOpen():
            if 0 <= recordNum < self.num_record:
                # Move the file pointer to the beginning of recordNum
                self.filestream.seek(recordNum * self.recordSize)
                
                # Read the key from the record
                key = self.filestream.read(self.Id_size).strip()

                if key == '_empty_':
                    # Empty record
                    return 0
                else:
                    # Non-empty record, read the rest of the fields
                    passengerId = key
                    fname = self.filestream.read(self.Fname_size).strip()
                    lname = self.filestream.read(self.Lname_size).strip()
                    age = self.filestream.read(self.Age_size).strip()
                    ticketNum = self.filestream.read(self.Tnum_size).strip()
                    fare = self.filestream.read(self.Fare_size).strip()
                    date = self.filestream.read(self.Date_size).strip()

                    return 1  # Successful read
            else:
                print("Invalid record number.")
                return -1  # Invalid record number
        else:
            print("Database is not open.")
            return -1  # Database is not open
     
    #write Record method           
    def writeRecord(self, recordNum, passengerId, fname, lname, age, ticketNum, fare, date):
        # Implement writeRecord method to write a record to the data file
        if self.filestream is not None:
            if 0 <= recordNum < self.num_record:
                # Move the file pointer to the beginning of the record
                self.filestream.seek(recordNum * self.recordSize)

                # Format the record data (assuming a fixed format)
                record_data = f"{passengerId},{fname},{lname},{age},{ticketNum},{fare},{date}"

                # Pad the record data if needed to match recordSize
                record_data = record_data.ljust(self.recordSize, '\0')

                # Write the record to the file
                self.filestream.write(record_data)

                print(f"Record {recordNum} updated successfully.")
                return 1  # 1 indicates successful update
            else:
                print("Invalid record number.")
                return -1  # -1 indicates invalid record number
    
    #update Record method        
    def updateRecord(self, passengerId, fname, lname, age, ticketNum, fare, date):
        # Implement updateRecord method
        if self.isOpen():
            recordNum, _, _, _, _, _, _, _ = self.binarySearch(passengerId)
            if recordNum != -1:
                # Call writeRecord to update the existing record
                return self.writeRecord(recordNum, passengerId, fname, lname, age, ticketNum, fare, date)
            else:
                print(f"Record with Passenger ID {passengerId} not found.")
                return False

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
    
    #Binary Search by record id
    def binarySearch(self, input_ID):
        low = 0
        high = self.record_size - 1
        found = False
        self.recordNum = None  # Initialize the insertion point

        while not found and high >= low:
            self.middle = (low + high) // 2
            self.getRecord(self.middle)
            mid_id = self.record["ID"]

            if mid_id.strip() == "_empty_":
                non_empty_record = self.findNearestNonEmpty(self.middle, low, high)
                if non_empty_record == -1:
                    # If no non-empty record found, set recordNum for potential insertion
                    self.recordNum = high 
                    print("Could not find record with ID..", input_ID)
                    return False

                self.middle = non_empty_record
                self.getRecord(self.middle)
                mid_id = self.record["ID"]
                if int(mid_id) > int(input_ID):
                    self.recordNum = self.middle - 1
                else:
                    self.recordNum = self.middle + 1

            if mid_id != "_empty_":
                try:
                    if int(mid_id) == int(input_ID):
                        found = True
                        self.recordNum = self.middle
                    elif int(mid_id) > int(input_ID):
                        high = self.middle - 1
                    elif int(mid_id) < int(input_ID):
                        low = self.middle + 1
                except ValueError:
                    # Handle non-integer IDs
                    high = self.middle - 1

        if not found and self.recordNum is None:
            # Set recordNum to high + 1 if no suitable spot is found
            self.recordNum = high 
            print("Could not find record with ID", input_ID)

        return found

    def findNearestNonEmpty(self, start, low_limit, high_limit):
        step = 1  # Initialize step size

        while True:
            # Check backward
            if start - step >= low_limit:
                self.getRecord(start - step)
                if self.record["ID"].strip() != "_empty_":
                    #print(self.record)
                    return start - step

            # Check forward
            if start + step <= high_limit:
                self.getRecord(start + step)
                if self.record["ID"].strip() != "_empty_":
                    #print(self.record)
                    return start + step

            # Increase step size and repeat
            step += 1

            # Terminate if beyond the search range
            if start - step < low_limit and start + step > high_limit:
                break

        return -1  # No non-empty record found

    #close the database
    def CloseDB(self):

        self.text_filename.close()

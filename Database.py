import csv
import os.path

class DB:

    #default constructor
    def __init__(self):
        self.filestream = None
        self.num_record = 0
        self.Id_size= 10
        self.Fname_size= 30
        self.Lname_size= 30
        self.Age_size= 10
        self.Tnum_size= 12
        self.Fare_size = 10
        self.Date_size = 20


    #create database
    def createDB(self,filename):
        #Generate file names
        csv_filename = filename + ".csv"
        text_filename = filename + ".data"

        # Read the CSV file and write into data files
        with open(csv_filename, "r") as csv_file:
            data_list = list(csv.DictReader(csv_file,fieldnames=('ID','fname','lname','age','ticketnum','fare','date')))

		# Formatting files with spaces so each field is fixed length, i.e. ID field has a fixed length of 10
        def writeDB(filestream, dict):
            filestream.write("{:{width}.{width}}".format(dict["ID"],width=self.Id_size))
            filestream.write("{:{width}.{width}}".format(dict["fname"],width=self.Fname_size))
            filestream.write("{:{width}.{width}}".format(dict["lname"],width=self.Lname_size))
            filestream.write("{:{width}.{width}}".format(dict["age"],width=self.Age_size))
            filestream.write("{:{width}.{width}}".format(dict["ticketnum"],width=self.Tnum_size))
            filestream.write("{:{width}.{width}}".format(dict["fare"],width=self.Fare_size))
            filestream.write("{:{width}.{width}}".format(dict["date"],width=self.Date_size))
            filestream.write("\n")

            #write an empty records
            filestream.write("{:{width}.{width}}".format('_empty_',width=self.Id_size))
            filestream.write("{:{width}.{width}}".format(' ',width=self.Fname_size))
            filestream.write("{:{width}.{width}}".format(' ',width=self.Lname_size))
            filestream.write("{:{width}.{width}}".format(' ',width=self.Age_size))
            filestream.write("{:{width}.{width}}".format(' ',width=self.Tnum_size))
            filestream.write("{:{width}.{width}}".format(' ',width=self.Fare_size))
            filestream.write("{:{width}.{width}}".format(' ',width=self.Date_size))
            filestream.write("\n")



        
        with open(text_filename,"w") as outfile:
            for dict in data_list:
                writeDB(outfile,dict)

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
            ticketnum = line[80:92]
            fare = line[92:102]
            date = line[102:122]
            self.record = dict({"ID":id,"fname":fname,"lname":lname,"age":age,"ticketnum":ticketnum,fare:"fare",date:"date"})
    
    #open record function
    def open(self, db_name):
        # Implement open method to read config file and open data file
        config_filename = db_name + ".config"
        data_filename = db_name + ".data"
        try:
            with open(config_filename, 'r') as config_file:
                self.numRecords, self.recordSize = map(int, config_file.read().splitlines())

            self.dataFileptr = open(data_filename, 'r+')
            return True
        except FileNotFoundError:
            return False
    
    #close record function
    def close(self):
        # Implement close method to close data file
        if self.dataFileptr is not None:
            self.dataFileptr.close()
            self.numRecords = 0
            self.recordSize = 0
            self.dataFileptr = None
            
    
    
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

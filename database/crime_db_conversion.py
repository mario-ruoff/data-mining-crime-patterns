from datetime import datetime
import sqlite3

FILE_NAME = "./chicago_crimes.tsv"
POLICE_FILE = './police.tsv'
CRIMES_FILE = "./crimes.db"

def strip_apostrophe(value):
    return value.replace('\'', '\\\'')

def update_database():
    con = sqlite3.connect(POLICE_FILE)   
    
    with open (FILE_NAME, 'r') as file:
        line = file.readline()
        line = strip_apostrophe(line)
        print(line)
        # execution_string = "drop table crime_stats"
        # cur.execute(execution_string)
        # con.commit()



def convert_rawdata_to_database():
    #2, 18

    con = sqlite3.connect(CRIMES_FILE)
    cur = con.cursor()
    print("Database connection successful!")

    datetime_format = "%m/%d/%Y %I:%M:%S %p"
    prev_line = ""

    with open (FILE_NAME, 'r') as file:
        line = file.readline()
        line = strip_apostrophe(line)
        print(line)
        # execution_string = "drop table crime_stats"
        # cur.execute(execution_string)
        # con.commit()


    # "11646166","JC213529","2018-09-01T00:01:00","082XX S INGLESIDE AVE","0810","THEFT,OVER $500","RESIDENCE",false,true,"0631","006,"8","44",06",,,2018,"2019-04-06T16:04:43",,,
        execution_string = ''' CREATE TABLE IF NOT EXISTS raw_crime_stats
                    (id INTEGER,
                    case_number TEXT,
                    date TEXT,
                    block TEXT,
                    iucr TEXT,
                    primary_type TEXT,
                    description TEXT,
                    location_description TEXT,
                    arrest BOOLEAN,
                    domestic BOOLEAN,
                    beat TEXT,
                    district TEXT,
                    ward INTEGER,
                    community_area TEXT,
                    fbi_code TEXT,
                    x_coordinate REAL,
                    y_coordinate REAL,
                    year INTEGER,
                    updated_on TEXT,
                    latitude REAL,
                    longitude REAL,
                    location TEXT)
    '''

        cur.execute(execution_string)
        con.commit()

        line_number = 0
        line_errors = []
        rows = []
        lines = file.readlines()
        print(len(lines))
        
        
        for line in lines:
            line_number += 1
            split_line = line.split('\t')
            if(len(split_line) != 22): # don't want to deal with this
                continue
            try: 
                split_line[2] = datetime.strptime(split_line[2], datetime_format).isoformat()
                split_line[18] = datetime.strptime(split_line[18], datetime_format).isoformat()
            except Exception as ex:
                print("Error in line ", line_number, str(ex), " continuing...")
                line_errors.append(line_number)
                continue
            #split_line[21] = ""

            execution_string = '''INSERT INTO crime_stats (
            id,
            case_number, 
            date, 
            block, 
            iucr, 
            primary_type, 
            description, 
            location_description, 
            arrest, 
            domestic, 
            beat, 
            district, 
            ward, 
            community_area, 
            fbi_code, 
            x_coordinate, 
            y_coordinate, 
            year, 
            updated_on, 
            latitude, 
            longitude)
            values(''' + \
            split_line[0] + ',' + \
            '\'' + split_line[1] + '\',' + \
            '\'' + split_line[2] + '\',' + \
            '\'' + split_line[3] + '\',' + \
            '\'' + split_line[4] + '\',' + \
            '\'' + split_line[5] + '\',' + \
            '\'' + split_line[6] + '\',' + \
            '\'' + split_line[7] + '\',' + \
            split_line[8] + ',' + \
            split_line[9] + ',' + \
            '\'' + split_line[10] + '\',' + \
            '\'' + split_line[11] + '\',' + \
            '\'' + split_line[12] + '\',' + \
            '\'' + split_line[13] + '\',' + \
            '\'' + split_line[14] + '\',' + \
            '\'' + split_line[15] + '\',' + \
            '\'' + split_line[16] + '\',' + \
            '\'' + split_line[17] + '\',' + \
            '\'' + split_line[18] + '\',' + \
            '\'' + split_line[19] + '\',' + \
            '\'' + split_line[20] + '\')' \
            
            rows.append(execution_string)
            try:
                cur.execute(execution_string)
            except Exception as ex:
                print("Error in line ", line_number, " " + str(ex))
                line_errors.append(line_number)
                continue

            if(line_number % 500000 == 0):
                print("Parsing line " , line_number)
                con.commit()

        con.commit()
        print("There were ", len(line_errors), " errors...")
        print(line_errors)
        cur.close()

    con.close()
from sys import argv
#if you don't have toml module, can install it using "sudo -H pip2 install toml"
#or "pip3 install toml twisted pymodbus"
import toml
#get the project directory from the first parameter
#if there is parameter passed in, set the project_directory as it, otherwise, set it to emtpty string 
import requests
import json

project_directory = argv[1] if len(argv) >1 else ""
#open(project_directory + "example.txt")

def start(project_directory):
    
    dbinfo,daily_sql,wells_sql  = openfiles(project_directory)

    #connect to the local database
    #use  python -m pip install mysql-connector-python to get install mysql-connection for python

    connect_to_db(dbinfo,daily_sql,wells_sql)
   
    #send data to ComboCurve api 
    
    

def openfiles(project_directory):
        #read "combocurve.toml" file
    try:
        with open(project_directory + "combocurve.toml") as f:
            dbconfig = toml.load(f)
            dbtype = dbconfig["connection"]["type"]
            dbinfo = dbconfig[dbtype]
        
    except:
        if project_directory: 
            print("Sorry, can't find 'combocurve.toml' file in "+ project_directory)
        else:
            print("Sorry, can't find 'combocurve.toml' file in the current directory")
        
        exit()
    #read sql files 
    sql_files = ["daily-productions.sql","wells.sql"]
    daily_sql, wells_sql = "",""
 
    #parse and store the sqls into thesql list
    for sql_file in sql_files:
        with open(project_directory + "resources/" + sql_file, 'r' ) as f:
            fread = f.read()
            sqls = fread.split(';')
            if sql_file == "daily-productions.sql": 
                daily_sql = "".join(" "+ sql for sql in sqls ) 
            else:
                wells_sql = "".join(" "+ sql for sql in sqls ) 
        
            f.close()
    #if there is no "daily-productions.sql" or "wells.sql" file, raise the error 
    if not daily_sql and not wells_sql :
        if project_directory: 
            raise Exception("Sorry, you don't have either 'daily-productions.sql' or 'wells.sql' in " + project_directory )
        else:
            raise Exception("Sorry, you don't have either 'daily-productions.sql' or 'wells.sql' in the current directory")
        
        exit()

    return dbinfo,daily_sql,wells_sql 




def connect_to_db(dbinfo,daily_sql,wells_sql):
    wells_url = "https://test-api.combocurve.com/v1/wells"
    daily_url = "https://test-api.combocurve.com/v1/daily-productions"

    x_api_key =  "AIzaSyCtjb6vep5dWTyrQNvoVBkKYWBH3WeGG2E"

    bear_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjUxYTc2MGJjMGZkOThiYWI5NTIzZjQwZDA5ZDY1ZTJkNGM2Mzg3Y2IifQ.eyJpc3MiOiJleHQtYXBpLWNvZGluZ0B0ZXN0LWNvbWJvY3VydmUuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLCJzdWIiOiJleHQtYXBpLWNvZGluZ0B0ZXN0LWNvbWJvY3VydmUuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLCJhdWQiOiJodHRwczovL3Rlc3QtYXBpLmNvbWJvY3VydmUuY29tIiwiaWF0IjoxNjM0MjE5MTY4LCJleHAiOjE2MzQ2NTExNjh9.MjZvJ5YdahFTcFSpJ1HFzcsmvo7K80dbP3VgcfAwurH3uOA5_4-paRxBXap7-p56WkxZ1TAcArd41GC-izMt5b3EsbrTVCIN-QpW83LTCfq1xnrzYMH9spmrMpHE02WK4kDjZPOj95cyP78rdNdSxIQEoQMYK5nGsncp8O3eD4i-I6jD-p19oIzbuZhFrjBRC0XAFti985y6M_Xo_4S8d4MlttyA2rlr95zmYm6IjqYbZ-rnm5kBrqQk3JEB9C168b6YZKAtjThM53ISBMVhHaOmc6kEmmKug2kO_pGN2mfHvh4vpwx1QNp8ljbXbz-Zv2NzNadCxZ_GCo1XRpQ-sA" 


    headers = {"x-api-key": x_api_key, "Authorization": "Bearer "+bear_token}
   # headers = {"x-api-key": x_api_key, "Authorization": bear_token}


    import mysql.connector
    from mysql.connector import errorcode
                
    user = str(dbinfo["user"])
    password = str(dbinfo["password"])
    host = str(dbinfo["host"])
    port = int(dbinfo["port"])

    try:
        cnx = mysql.connector.connect(
            user=user,
            password= password,
            host=host,
            port= port)
            #auth_plugin='mysql_native_password')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        
        exit()

    print("successfully connected to the database.....")

    cursor = cnx.cursor(buffered=True)
    
    
    #save the wells data into wells_dataset and daily production data into daily_dataset
    #use size to control how many records each time to get from database 
    size = 100
    #use round to control how many rounds to fetch and send data
    round = 10
    daily_dataset = []

    if wells_sql:
        cursor.execute(wells_sql)
        while round>0: 
            
            round-=1
            wells_dataset = []
            #use fetchmany to get  size numbers of records each time, and repeatly 
            #it records the position of record fetching
            records = cursor.fetchmany(size)

            
            for dataSource,chosenID,wellName,api14,perfLateralLength,county,state,country in records:
                well = [dataSource,chosenID,wellName,api14,perfLateralLength,county,state,country]
 
                #if well is empty, means the database does not have 1000 records, exit the loop
                if not well:
                    break 
                wells_dataset.append(well)    
            
            if not well:
                break 
            send_to_api(daily_dataset,wells_dataset,wells_url,daily_url,headers)
    #let send_to_api only deals with daily_dataset 
    wells_dataset = []
    round= 2

    if daily_sql:
        cursor.execute(daily_sql)
        while round>0: 
            round-=1
            daily_dataset = []
            records = cursor.fetchmany(size)
    
            for dataSource, chosenID, oil,gas,water,date in records:
                daily = [dataSource,chosenID,oil,gas,water,date]
                if not daily:
                    break
                daily_dataset.append(daily)
            
            if not daily:
                break
            send_to_api(daily_dataset,wells_dataset,wells_url,daily_url,headers)

    #close the db connection
    cnx.close()

def send_to_api(daily_dataset, wells_dataset,wells_url,daily_url,headers):


    if wells_dataset:
        for well in wells_dataset:
            print(well)

            well_data = {"dataSource":well[0],"chosenID":well[1],"wellName":well[2],
            "api14":well[3],"perfLateralLength":well[4], "county":well[5],
            "state":well[6],"country":well[7]}
            
           # response = requests.put(wells_url, data=json.dumps(well_data,indent=4, sort_keys=True, 
           # default=str), headers=headers)
            response = requests.put(wells_url, json=well_data, headers=headers)
            print(response.json() )
            print(response.status_code)
    
    if daily_dataset:
        for daily in daily_dataset:
            print(daily)

            daily_data = {"dataSource":daily[0],"chosenID":daily[1],"oil":daily[2],
            "gas":daily[3],"water":daily[4], "date":daily[5] }
            
            response = requests.put(daily_url, data=json.dumps(daily_data,indent=4, sort_keys=True, default=str), headers=headers)

            print(response.json() )
            print(response.status_code)


start(project_directory)

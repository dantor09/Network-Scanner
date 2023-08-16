import mysql.connector
import pandas as pd

class DatabaseConnection:
    
    def __init__(self, username, password, host, database):
        self.user = username
        self.password = password
        self.host = host
        self.database = database
        self.tableName = "tcpScans"
    
    def table_exists(self, tableName):
    
        self.cursor.execute(f"""SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = N'{tableName}'""")
        tableInformation = self.cursor.fetchall()
        return 0 if len(tableInformation) == 0 else len(tableInformation)
   
    def get_database_columns(self):

        self.cursor.execute(f"""SELECT COLUMN_NAME
                               FROM INFORMATION_SCHEMA.COLUMNS
                               WHERE TABLE_NAME = N'{self.tableName}'""")
       
        tcpColumnsList = self.cursor.fetchall()
        return tcpColumnsList[3:]
    def write_to_database(self, fileName, ports):
        
        try:
            cnx = mysql.connector.connect(
                    user = self.user,
                    password = self.password,
                    host = self.host,
                    database = self.database
                    )
        except Exception as e:
            print("Something went wrong with the connection to " + str(self.database))
        else:
            data = pd.read_csv(fileName, sep = ",")
            df = pd.DataFrame(data)
             
            self.cursor = cnx.cursor()
             
            #if self.table_exists(self.tableName): 
            
            localPorts = [string[3:] for string in ports]
            intLocalPorts = [int(number) for number in localPorts]
            
            minValue = min(intLocalPorts)
            maxValue = max(intLocalPorts)

            self.tableName = str(len(intLocalPorts)) + "_" + self.tableName + str(minValue)+ "_" + str(maxValue) 
            tcpColumns = self.get_database_columns()
            
            tcpColumnsPorts = [string[0][3:] for string in tcpColumns]
            tcpColumnsPorts = [int(string) for string in tcpColumnsPorts]
            tcpColumnsPorts.sort()
            tcpColumnsPorts = [str(string) for string in tcpColumnsPorts]            
            if tcpColumnsPorts == localPorts or len(tcpColumnsPorts) == 0 :
                print("THEY ALL MATCH")
            else:
                print("THEY DO NOT MATCH")
            
        
            # SQL to create the dynamic table
            baseCreateTableSQL = f"""
            CREATE TABLE IF NOT EXISTS {self.tableName} (
            DateTime datetime,
            Host varchar(50),
            Ping varchar(50),
            """
            # Generating columns for each port
            TCPPortsColumnSQL = ", ".join([f"{port} varchar(8)\n" for port in ports])

            # Final SQL for table creation
            CreateTableSQL = baseCreateTableSQL + TCPPortsColumnSQL + ")"

            self.cursor.execute(CreateTableSQL)

            # SQL to insert data into the table
            baseInsertSQL = f"""
            INSERT INTO {self.tableName} 
                (DateTime, Host, Ping, """
            
            # Generating columns for each port
            TCPPortsColumnSQL = ",".join([port for port in ports])
            SQLPlaceholders = ", ".join(["%s"] * (len(ports) + 3))
            
            insertSQL = baseInsertSQL + TCPPortsColumnSQL + ") VALUES (" + SQLPlaceholders + ")"
            
            for row in df.itertuples(index = False):
                self.cursor.execute(insertSQL,
                            tuple(row[0:])
                            )
            cnx.commit()

            cnx.close()

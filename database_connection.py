import mysql.connector
import pandas as pd

class DatabaseConnection:
    
    def __init__(self, username, password, host, database):
        self.user = username
        self.password = password
        self.host = host
        self.database = database
        
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
             
            # Create the table if it exists
            cursor = cnx.cursor()
            
            cursor.execute("""SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = N'scans'""")

            databaseTableColumns = cursor.fetchall()
            

            if len(array) == 0:
                print("The table does not exist")
            else:
                
                print("The table exists")
            cursor.execute("""SELECT COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = N'scans'""")
            
            array_list = cursor.fetchall()
            print(array_list)
            print("JFHDKJFHJKDSH")
            for column in array_list:
                if column[0] == "TCP22":
                    print("Found tcp22")
                else:
                    print("not found")
            
            # SQL to create the dynamic table
            baseCreateTableSQL = """
            CREATE TABLE IF NOT EXISTS scans (
            DateTime datetime,
            Host varchar(50),
            Ping varchar(50),
            """
            # Generating columns for each port
            TCPPortsColumnSQL = ", ".join([f"{port} varchar(8)\n" for port in ports])

            # Final SQL for table creation
            CreateTableSQL = baseCreateTableSQL + TCPPortsColumnSQL + ")"

            cursor.execute(CreateTableSQL)

            # SQL to insert data into the table
            baseInsertSQL = """
            INSERT INTO scans 
                (DateTime, Host, Ping, """
            
            # Generating columns for each port
            TCPPortsColumnSQL = ",".join([port for port in ports])
            SQLPlaceholders = ", ".join(["%s"] * (len(ports) + 3))
            
            insertSQL = baseInsertSQL + TCPPortsColumnSQL + ") VALUES (" + SQLPlaceholders + ")"
            
            for row in df.itertuples(index = False):
                cursor.execute(insertSQL,
                            tuple(row[0:])
                            )
            cnx.commit()

            cnx.close()

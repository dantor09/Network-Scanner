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

            # Create the table if it exists
            cursor = cnx.cursor()
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

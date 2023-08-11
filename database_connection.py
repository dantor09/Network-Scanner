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

            base_sql = "CREATE TABLE IF NOT EXISTS scans (DateTime datetime,Host varchar(50),Ping varchar(50),"
            sql_ports = [f"{port} varchar(10)" for port in ports]
            sql_ports = ",".join(sql_ports)

            sql = base_sql + sql_ports +")"

            cursor = cnx.cursor()
            cursor.execute(sql)
            
            placeholders = ",".join(["%s"] * (len(ports) + 3))
            temp = ",".join([port for port in ports])
            base_insert = "INSERT INTO scans(Datetime , Host, Ping," + temp + " ) VALUES ( " + placeholders + ")"
            print(base_insert)
            for row in df.itertuples(index = False):
                cursor.execute(base_insert,
                            tuple(row[0:])
                            )
            cnx.commit()
            cnx.close()

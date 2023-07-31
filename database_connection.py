class DatabaseConnection:
    
    def __init__(self, username, password, host, database):
        self.user = username
        self.password = password
        self.host = host
        self.database = database
        
    def write_to_database(self, fileName):
        
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
            cursor = cnx.cursor()
            cursor.execute('''
                                CREATE TABLE IF NOT EXISTS scans(
                                DateTime datetime,
                                Host varchar(50),
                                Ping varchar(50),
                                TCP19 varchar(50),
                                TCP21 varchar(10),
                                TCP22 varchar(10),
                                TCP23 varchar(10),
                                TCP25 varchar(10),
                                TCP80 varchar(10),
                                TCP110 varchar(10),
                                TCP137 varchar(10),
                                TCP138 varchar(10),
                                TCP139 varchar(10),
                                TCP143 varchar(10),
                                TCP179 varchar(10),
                                TCP389 varchar(10),
                                TCP443 varchar(10),
                                TCP445 varchar(10),
                                TCP902 varchar(10),
                                TCP903 varchar(10),
                                TCP993 varchar(10),
                                TCP995 varchar(10),
                                TCP1080 varchar(10),
                                TCP1433 varchar(10),
                                TCP3306 varchar(10),
                                TCP3389 varchar(10),
                                TCP5900 varchar(10)
                                )
                            ''' )



            for row in df.itertuples(index = False):
                cursor.execute('''
                            INSERT INTO scans(DateTime,Host,Ping,TCP19,TCP21,TCP22,TCP23,TCP25,TCP80,TCP110,TCP137,TCP138,TCP139,TCP143,TCP179,TCP389,TCP443,TCP445,TCP902,TCP903,TCP993,TCP995,TCP1080,TCP1433,TCP3306,TCP3389,TCP5900)
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            ''',
                            tuple(row[0:])
                            )
            cnx.commit()
            cnx.close()
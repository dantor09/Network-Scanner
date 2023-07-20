import ipaddress  #Allows for IP address manipulation
import sys
import os 
import datetime
import csv 
import socket
import pandas as pd 
import pyodbc 

class DatabaseConnection:
    pass

class CSV:
    def __init__(self,fileName):
        self.df = pd.DataFrame(columns=["Date/Time","Host","Ping","TCP/19","TCP/21","TCP/22","TCP/23","TCP/25","TCP/80","TCP/110","TCP/137","TCP/138","TCP/139","TCP/143","TCP/179","TCP/389","TCP/443","TCP/445","TCP/902","TCP/903","TCP/993","TCP/995","TCP/1080","TCP/1433","TCP/3606","TCP/3389","TCP/5900"])
        self.fileName = fileName
        self.csvRows = []
    
    def write_to_dataframe(self):
        self.df.loc[len(self.df)] = self.csvRows 

        self.csvRows = []
    
    def write_to_csv(self):
        self.df.to_csv(self.fileName,sep=",",index=False)

class Network:
    
    def __init__(self, ipAddress, fileName):
        self.csv = CSV(fileName)
        print("This is the CSV: ")
        print(self.csv)

        self.ipAddress = ipaddress.ip_interface(ipAddress)
        self.ipNetwork = ipaddress.ip_network(str(self.ipAddress.network))
        self.ports = [19,21,22,23,25,80,110,137,138,139,143,179,389,443,445,902,903,993,995,1080,1433,3306,3389,5900]
         
    @staticmethod
    def is_valid_ip(ipAddress):
        valid = []

        try:
            valid = ipaddress.ip_interface(ipAddress)
        except ValueError:
            print(ipAddress + " is not valid")
        
        return valid
    
    def test_tcp(self, ip):

        for index, port in enumerate(self.ports):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.002) 
            result = sock.connect_ex((str(ip),port))
        
            # SUCCESSFU
            if result == 0:
                print ("Port: " + str(port) + " is open on " + str(ip))
                self.csv.csvRows.append("Open")
            else:
                print ("Port: " + str(port) + " is closed on " + str(ip))
                self.csv.csvRows.append("Closed")
            sock.close()
        self.csv.write_to_dataframe()

    def ping_network(self):       
        self.csv.csvRows = []

        for ip in self.ipNetwork:
            
            startTime = datetime.datetime.now().replace(microsecond=0)
            response = os.system("ping -c 1 -W 5 " + str(ip) + " > /dev/null")
            pinged = "no"
            self.csv.csvRows.append(str(startTime))
            self.csv.csvRows.append(str(ip))
        
            if response == 0:
                print("0 Connection accepted from ", str(ip))
                pinged = "yes"
            elif response == 1: 
                print("1 Timeout from ", str(ip))
                pinged = "timeout"
            else:
                print("2 Refused from ", str(ip))
                pinged = "no"
            
            self.csv.csvRows.append(pinged)
            
            self.test_tcp(ip)

        self.csv.write_to_csv()

    def connection(self):
        data = pd.read_csv(self.fileName,  sep=",")
        df = pd.DataFrame(data)
        
        #creates connection object

        database_conn = pyodbc.connect(
                #not tested yet
                driver = r'/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.9.so.1.1',
                host = "localhost",
                user = input("Username: "),
                password = input("Password: ")
            )

        #executes SQL statements

        cursor = database_conn.cursor()

        cursor.execute('''
                        Create table information(
                        information_date/time int primary key,
                        information_host nvarchar(50),
                        ping int,
                        information_TCP/19 int,
                        information_TCP/21 int,
                        information_TCP/22 int,
                        information_TCP/23 int,
                        information_TCP/25 int,
                        information_TCP/80 int,
                        information_TCP/110 int,
                        information_TCP/137 int,
                        information_TCP/138 int,
                        information_TCP/139 int,
                        information_TCP/389 int,
                        information_TCP/445 int,
                        information_TCP/902 int,
                        information_TCP/903 int,
                        information_TCP/993 int,
                        information_TCP/995 int,
                        information_TCP/1080 int,
                        information_TCP/1433 int,
                        information_TCP/3606 int,
                        information_TCP/3389 int,
                        information_TCP/5900 int
                        )
                   ''' )

        for row in df.itertuples():
            cursor.execute('''
                        INSERT INTO information (information_date/time, information_host, ping)
                        VALUES(, , ,)
                        ''',
                        row.information_date/time,
                        row.information_host,
                        row.ping
                        )
        database_conn.commit()

ipAddress = input("IP Address: ")
while not Network.is_valid_ip(ipAddress):
    ipAddress = input("IP Address: ")

network1 = Network(ipAddress,"network1.csv")

network1.ping_network()







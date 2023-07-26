import ipaddress  #Allows for IP address manipulation
import sys
import os 
import datetime
import csv 
import socket
import pandas as pd 
import mysql.connector

class DatabaseConnection:
    def __init__(self, user, password):

        self.user = user
        self.password = password
        self.host = "127.0.0.1"
        self.database = "scans"
        self.cnx = mysql.connector.connect

    def connection_obj(self):
        self.cnx =(mysql.connector.connect(self.user, self.password, self.host, self.database))
        self.data = pd.read_csv(self.csv.fileName, sep = ";")
        self.df = pd.DataFrame(self.data)

        
    def create_table(self):
        self.cursor = cnx.cursor()
        self.cursor.execute('''
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



    def insert_to_table(self):
        for row in df.itertuples(index = False):
            cursor.execute('''
                        INSERT INTO scans(DateTime,Host,Ping,TCP19,TCP21,TCP22,TCP23,TCP25,TCP80,TCP110,TCP137,TCP138,TCP139,TCP143,TCP179,TCP389,TCP443,TCP445,TCP902,TCP903,TCP995,TCP1080,TCP1433,TCP3306,TCP3389,TCP5900)
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ''',
                        tuple(row[0:])
                        )
        cnx.commit()
        cnx.close()


class CSV:
    def __init__(self,fileName):
        self.df = pd.DataFrame(columns=["Date/Time","Host","Ping","TCP/19","TCP/21","TCP/22","TCP/23",
                                        "TCP/25","TCP/80","TCP/110","TCP/137","TCP/138","TCP/139","TCP/143",
                                        "TCP/179","TCP/389","TCP/443","TCP/445","TCP/902","TCP/903",
                                        "TCP/993","TCP/995","TCP/1080","TCP/1433","TCP/3306","TCP/3389","TCP/5900"])
        self.fileName = fileName
        self.csvRows = []
    
    def write_to_dataframe(self):
        self.df.loc[len(self.df)] = self.csvRows 
        self.csvRows = []
    
    def write_to_csv(self):
        self.df.to_csv(self.fileName, sep=",", index=False)

class Network:
    
    groupSize = {128:[25,17,9,1],
                 64:[26,18,10,2],
                 32:[27,19,11,3],
                 16:[28,20,12,4],
                 8:[29,21,13,5],
                 4:[30,22,14,6],
                 2:[31,23,15,7],
                 1:[32,24,16,8]}
    
    def __init__(self, ipAddress, fileName="default.csv"):
        self.csv = CSV(fileName)
        self.parse_ip(ipAddress)
        self.fileName = fileName
        self.ipAddress = ipaddress.ip_interface(ipAddress)
        self.ipNetwork = ipaddress.ip_network(str(self.ipAddress.network))
        self.ports = [19,21,22,23,25,80,110,137,138,139,143,179,389,443,445,902,903,993,995,1080,1433,3306,3389,5900]
    
    def parse_ip(self,ipAddress):
        self.ipOctets = []
        #print("octetList type: " + str(type(octetList)))
        self.ip = ipAddress.split("/")[0]
        self.CIDR = int(ipAddress.split("/")[1])
        self.octet1 = int(self.ip.split(".")[0])
        self.octet2 = int(self.ip.split(".")[1])
        self.octet3 = int(self.ip.split(".")[2])
        self.octet4 = int(self.ip.split(".")[3])

        self.ipOctets.append(self.octet1)
        self.ipOctets.append(self.octet2)
        self.ipOctets.append(self.octet3)
        self.ipOctets.append(self.octet4)
        self.ipOctets.append(self.CIDR)

    def get_ip_address(self):
        return str(self.ipOctets[0]) + "." + str(self.ipOctets[1]) + "." + str(self.ipOctets[2]) + "." + str(self.ipOctets[3])
    
    def get_octet_block(self):

        octetIndex = 0
        CIDR = int(self.CIDR)
        #print(type(self.CIDR))
        if CIDR in range(1,9):
            octetIndex = 0
        if CIDR in range(9,17):
            octetIndex = 1
        if CIDR in range(17,25):
            octetIndex = 2
        if CIDR in range(25,33):
            octetIndex = 3

        return octetIndex

    def __get_network_size(self):
        networkSize = 0
        
        for key, values in Network.subNetworkSize.items():
            if int(self.CIDR) in values:
                networkSize = key
        return networkSize
    
    def get_network(self):
        
        networkSize = self.__get_network_size()
         
        #print("this is the network size: " + str(networkSize))
        startingNetworkIP = 0
        previousStartingNetworkIP = startingNetworkIP
        
        octetIndex = self.get_octet_block() 

        #print("Before the loop")
        while startingNetworkIP <= self.ipOctets[octetIndex]:
            return self.get_ip_address()

    def get_broadcast(self):
        currentSubNetworkIP = 0
        previousSubNetworkIP = currentSubNetworkIP
        
        octetIndex = self.get_octet_index() 

        while currentSubNetworkIP <= self.ipOctets[octetIndex]:
            previousSubNetworkIP = currentSubNetworkIP
            currentSubNetworkIP += self.networkSize

        self.ipOctets[octetIndex] = previousSubNetworkIP + self.networkSize - 1
        
        while (octetIndex + 1) < len(self.ipOctets):
            self.ipOctets[octetIndex + 1] = 255
            octetIndex += 1
        
        return self.get_ip_address()    
    
    def produce_ip_range(self):
        
        networkCapacity = 2**(32 - self.CIDR)
        print("This is the networkCapacity: " + str(networkCapacity) + " for a CIDR of " + str(self.CIDR))

        self.get_network()
        octetIndex = self.get_octet_index() + 1
        previousSubNetworkIP, currentSubNetworkIP = 0, 0 

        while currentSubNetworkIP < self.networkSize:
            print(self.ipOctets[0:4])
            self.ipOctets[octetIndex] += 1
            if self.ipOctets[octetIndex] == 256:
                self.ipOctets[octetIndex] = 0
                self.ipOctets[octetIndex - 1] += 1
                networkCapacity -= 256
                if networkCapacity <= 0:
                    break
                else:
                    if self.ipOctets[octetIndex - 1] >= 256:
                        self.ipOctets[octetIndex - 2] += 1

                
                



    def get_ip_range(self):

        currentSubNetworkIP = 0
        previousSubNetworkIP = currentSubNetworkIP
        
        octetIndex = self.get_octet_index() 

        while currentSubNetworkIP <= self.ipOctets[octetIndex]:
            previousSubNetworkIP = currentSubNetworkIP
            currentSubNetworkIP += self.networkSize

        self.ipOctets[octetIndex] = previousSubNetworkIP + 1
        
        while (octetIndex + 1) < len(self.ipOctets):
            self.ipOctets[octetIndex + 1] = 254
            octetIndex += 1
        
        return self.get_ip_address() + " - " + self.get_broadcast()

    @staticmethod
    def is_valid_ip(ipAddress):
    
        valid = True
        
        try:
            ip = ipAddress.split("/")[0]
            CIDR = int(ipAddress.split("/")[1])
            octet1 = int(ip.split(".")[0])
            octet2 = int(ip.split(".")[1])
            octet3 = int(ip.split(".")[2])
            octet4 = int(ip.split(".")[3])
        except ValueError:
            print("Invalid IP")
            valid = False
        except Exception as e:
            print("Something went wrong")
            print(e)
            valid = False
        else:

            if CIDR >= 33 or CIDR <= 0:
                valid = False
            if octet1 >= 256 or octet1 < 0:
                valid = False
            if octet2 >= 256 or octet2 < 0:
                valid = False
            if octet3 >= 256 or octet3 < 0:
                valid = False 
            if octet4 >= 256 or octet4 < 0:
                valid = False
        
        return valid
    
    def test_tcp(self, ip):

        for index, port in enumerate(self.ports):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.002) 
            result = sock.connect_ex((str(ip),port))
        
            # SUCCESSFUL
            if result == 0:
                print ("Port: " + str(port) + " is open on " + str(ip))
                self.csv.csvRows.append("Open")
            else:
                df = pd.DataFrame(data)
        

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ipCIDR = sys.argv[1]
    else:
        ipCIDR = input("Enter IP: ")
    while not Network.is_valid_ip(ipCIDR):
        ipCIDR = input("Enter IP: ")
    #database = DatabaseConnection("daniel","93263","information")
    network1 = Network(ipCIDR,"network1.csv")

    #network1.produce_ip_range()
    #network1.ping_network()
    #network1.connection()

    DatabaseConnection1 = DatabaseConnection("roselyn", "d2eadf8083")
    DatabaseConnection1.connection_obj()
    DatabaseConnection1.create_table()
    DatabaseConnection1.insert_to_table()






import ipaddress  #Allows for IP address manipulation
import sys
import os 
import datetime
import csv 
import socket
import pandas as pd 
#import mysql.connector

class DatabaseConnection:
    pass

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
    
    subNetworkSize = {128:[25,17,9,1],
                      64:[26,18,10,2],
                      32:[27,19,11,3],
                      16:[28,20,12,4],
                      8:[29,21,13,5],
                      4:[30,22,14,6],
                      2:[31,23,15,7],
                      1:[32,24,16,8]}
    
    def __init__(self, ipAddress, fileName="default.csv", dataBaseObject=None):
        self.csv = CSV(fileName)
        self.parse_ip(ipAddress)
        self.networkSize = self.__get_network_size()
        self.ports = [19,21,22,23,25,80,110,137,138,139,143,179,389,443,445,902,903,993,995,1080,1433,3306,3389,5900]

    def parse_ip(self,ipAddress):
        self.ipOctets = []
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
        
    def get_octet_index(self):
        octetIndex = 0
        CIDR = int(self.CIDR)
        
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
         
        previousSubNetworkIP, currentSubNetworkIP = 0, 0
        octetIndex = self.get_octet_index() 

        ''' Find what subnetwork the ip portion of the IP address is in'''
        while currentSubNetworkIP <= self.ipOctets[octetIndex]:
            previousSubNetworkIP = currentSubNetworkIP
            currentSubNetworkIP += self.networkSize

        ''' Set the network portion of the IP address to the subnetwork'''
        self.ipOctets[octetIndex] = previousSubNetworkIP
 
        ''' Set the rest of the octets to 0'''
        while (octetIndex + 1) < len(self.ipOctets):
            self.ipOctets[octetIndex + 1] = 0
            octetIndex += 1
        
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
    
    def decode_ip(self, netInteger):
        
        octet1 = int(netInteger / (256*256*256))    
        octet2 = int((netInteger % (256*256*256)) / (256*256))
        octet3 = int((netInteger % (256*256)) / 256)
        octet4 = int(netInteger % 256)
    
        return str(octet1) + '.' + str(octet2) + '.' + str(octet3) + '.' + str(octet4)
    
    def get_ip_range(self):
        self.get_network()
        netInteger = (self.ipOctets[0]*256*256*256) + (self.ipOctets[1]*256*256) + (self.ipOctets[2]*256) + self.ipOctets[3]
        start = netInteger

        #    Convert netmask to integer
        print("This is the value of CIDR: " + str(self.CIDR))
        maskBits = self.CIDR
        hosts = 2**(32-maskBits)
        print("These are the amount of hosts you can have: " + str(hosts))
        end = netInteger + hosts

        return start, end

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
                print ("Port: " + str(port) + " is closed on " + str(ip))
                self.csv.csvRows.append("Closed")
            sock.close()
        self.csv.write_to_dataframe()
    
    def ping_ip(self, ip):       
        self.csv.csvRows = []
        
        startTime = datetime.datetime.now().replace(microsecond=0)
        response = os.system("ping -c 1 -W 5 " + str(self.decode_ip(ip)) + " > /dev/null")
        pinged = "no"
        self.csv.csvRows.append(str(startTime))
        self.csv.csvRows.append(str(self.decode_ip(ip)))
        
        if response == 0:
            print("0 Connection accepted from ", str(self.decode_ip(ip)))
            pinged = "yes"
        elif response == 1: 
            print("1 Timeout from ", str(self.decode_ip(ip)))
            pinged = "timeout"
        else:
            print("2 Refused from ", str(self.decode_ip(ip)))
            pinged = "no"
            
        self.csv.csvRows.append(pinged)
        self.test_tcp(self.decode_ip(ip))
        self.csv.write_to_csv() 
    
    def connection(self):
        
        data = pd.read_csv(self.csv.fileName,  sep=",")
        df = pd.DataFrame(data)

        cnx = mysql.connector.connect(user="", 
                                      password="", 
                                      host="127.0.0.1", 
                                      database="information")

        cursor = cnx.cursor()
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS scans(
                        DateTime datetime,
                        Host varchar(50),
                        Ping varchar(50),
                        TCP19 varchar(10),
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

        for row in df.itertuples(index=False):
            cursor.execute('''
                        INSERT INTO scans (DateTime, Host, Ping, TCP19, TCP21, TCP22,TCP23,TCP25,TCP80,TCP110,TCP137,TCP138,TCP139,TCP143,TCP179,TCP389,TCP443,TCP445,TCP902,TCP903,TCP993,TCP995,TCP1080,TCP1433,TCP3306,TCP3389,TCP5900)
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ''',
                        tuple(row[0:])
                        )
        cnx.commit()
        cnx.close()

if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        ipCIDR = sys.argv[1]
    else:
        ipCIDR = input("Enter IP: ")

    while not Network.is_valid_ip(ipCIDR):
        ipCIDR = input("Enter IP: ")

    network1 = Network("196.168.1.3/30", "example.csv")
    







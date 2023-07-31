import sys
import os 
import datetime
import socket
import pandas as pd 
from database_connection import DatabaseConnection
from csv_handler import CSV

class Network:
    
    subNetworkSize = {128:[25,17,9,1],
                      64:[26,18,10,2],
                      32:[27,19,11,3],
                      16:[28,20,12,4],
                      8:[29,21,13,5],
                      4:[30,22,14,6],
                      2:[31,23,15,7],
                      1:[32,24,16,8]}
    
    def __init__(self, ipAddress, fileName="default.csv", databaseConnection=None):
        
        '''Network class has a database connection object and a csv file writer object
           they will serve as components of the Network class'''
        self.database = databaseConnection
        self.csv = CSV(fileName)
        
        '''parse_ip takes an ip address with CIDR and sets up the member variables of Network
           which include ipOctets list which holds each octet and the CIDR in different indexes.'''
        
        self.__parse_ip(ipAddress)   
        self.networkSize = self.__get_network_size() 
        self.ports = [19,21,22,23,25,80,110,137,138,139,143,179,389,443,445,902,903,993,995,1080,1433,3306,3389,5900]
    
    def __parse_ip(self,ipAddress):
        self.ipOctets = []
        self.networkIpOctets = []
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
        self.networkIpOctets = self.ipOctets.copy()
        


    def get_ip_address(self):
        return str(self.ipOctets[0]) + "." + str(self.ipOctets[1]) + "." + str(self.ipOctets[2]) + "." + str(self.ipOctets[3])
     
    def get_octet_index(self):
        '''Obtain the octet index under which the CIDR lands on'''
        self.octetIndex = 0
        CIDR = int(self.CIDR)
        
        if CIDR in range(1,9): self.octetIndex = 0
        if CIDR in range(9,17): self.octetIndex = 1
        if CIDR in range(17,25): self.octetIndex = 2
        if CIDR in range(25,33): self.octetIndex = 3

        return self.octetIndex

    def __get_network_size(self):
        networkSize = 0
        
        for key, values in Network.subNetworkSize.items():
            if int(self.CIDR) in values: networkSize = key
        return networkSize
    
    def __get_subnetwork_ip(self):
        
        """Returns the network address of the current IP address"""        
        previousSubNetworkIP, currentSubNetworkIP = 0, 0
        self.octetIndex = self.get_octet_index()

        """Get the network address of the current IP address"""
        while currentSubNetworkIP <= self.ipOctets[self.octetIndex]:
            previousSubNetworkIP = currentSubNetworkIP
            currentSubNetworkIP += self.networkSize

        return previousSubNetworkIP

    def get_network(self):
        '''Tested'''
        self.networkIpOctets[self.octetIndex] = self.__get_subnetwork_ip()

        """Set the remaining octets to 0"""
        while(self.octetIndex + 1) < len(self.networkIpOctets):
            self.networkIpOctets[self.octetIndex + 1] = 0
            self.octetIndex += 1

        return str(self.networkIpOctets[0]) + "." + str(self.networkIpOctets[1]) + "." + str(self.networkIpOctets[2]) + "." + str(self.networkIpOctets[3])

    def get_broadcast_ip(self):

        self.ipOctets[self.octetIndex] = self.__get_subnetwork_ip() + self.networkSize - 1
        
        while (self.octetIndex + 1) < len(self.ipOctets):
            self.ipOctets[self.octetIndex + 1] = 255
            self.octetIndex += 1
        
        return self.get_ip_address()    
    
    @staticmethod
    def decode_ip(ipInteger):
        '''Tested''' 
        if type(ipInteger) == str:
            try:
                ipInteger = int(ipInteger)
            except Exception as e:
                print("Unable to turn " + str(ipInteger) + " to an integer")
                print(e)
        
        octet1 = int(ipInteger / (256*256*256))    
        octet2 = int((ipInteger % (256*256*256)) / (256*256))
        octet3 = int((ipInteger % (256*256)) / 256)
        octet4 = int(ipInteger % 256)
         
        return str(octet1) + '.' + str(octet2) + '.' + str(octet3) + '.' + str(octet4)
    
    def get_ip_range(self):
        
        self.get_network()
        ipInteger = (self.networkIpOctets[0]*256*256*256) + (self.networkIpOctets[1]*256*256) + (self.networkIpOctets[2]*256) + self.networkIpOctets[3]
        start = ipInteger
        hosts = 2**(32-self.CIDR)
        end = ipInteger + hosts - 1

        return start, end

    @staticmethod
    def is_valid_ip(ipAddress):
    
        valid = True
        
        try:
            ip, CIDR = ipAddress.split("/")
            CIDR = int(CIDR)
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
            if CIDR >= 33 or CIDR <= 0: valid = False
            if octet1 >= 256 or octet1 < 0: valid = False
            if octet2 >= 256 or octet2 < 0: valid = False
            if octet3 >= 256 or octet3 < 0: valid = False
            if octet4 >= 256 or octet4 < 0: valid = False
        
        return valid
    
    def test_tcp(self, ip):

        for port in self.ports:
            result = self.scan_port(ip, port)

            # SUCCESSFUL
            if result == 0: self.csv.csvRows.append("Open")
            else: self.csv.csvRows.append("Closed")

        self.csv.write_to_dataframe()
        
    def scan_port(self, ip, port):
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.002) 
        result = sock.connect_ex((str(ip), port))
        sock.close()

        return result
    
    def ping_ip(self, ip):     


        if type(ip) == int:
            try:
                ip = self.decode_ip(ip)
            except Exception as e:
                print(e)
                print("IP defaulted to 0.0.0.0")
                ip ="0.0.0.0"
        
        self.csv.csvRows = []
        
        startTime = datetime.datetime.now().replace(microsecond=0)
        self.csv.csvRows.append(str(startTime))
        response = os.system("ping -c 1 -W 5 " + str(ip) + " > /dev/null")
        pinged = "no"
        self.csv.csvRows.append(str(ip))
        
        if response == 0: pinged = "yes"
        elif response == 1: pinged = "timeout"
        else: pinged = "no"
            
        self.csv.csvRows.append(pinged)
        self.test_tcp(ip)
        self.csv.write_to_csv()
   
    def ping_network(self):
        self.csv.csvRows = []
        start, stop = self.get_ip_range()
        
        while start <= stop:
            ip = self.decode_ip(start)
            self.ping_ip(ip)            
            start += 1

    def write_to_database(self):
        self.database.write_to_database(self.csv.fileName)
        
if __name__ == "__main__":

    if len(sys.argv) > 1: ipCIDR = sys.argv[1]
    else: ipCIDR = input("Enter IP: ")
    
    while not Network.is_valid_ip(ipCIDR):
        ipCIDR = input("Enter IP: ")
 
    db = DatabaseConnection("","","","")
    network = Network(ipCIDR,"network1.csv",db)
    network.ping_network()
    if network.scan_port(network.ip, 22) == 0:
        print("Port 22 is open")
    else: 
        print("Port 22 is closed")

    network.write_to_database()

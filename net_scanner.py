import ipaddress  #Allows for IP address manipulation
import sys
import os 
import datetime
import csv 
import socket

protocol = ["Chargen","FTP","SSH","Telnet","SMTP","HTTP","POP3","NETBIOS","NETBIOS","NETBIOS","IMAP","BGP","LDAP","HTTPS","Microsoft directory services","VMware ESX","VMware ESX","IMAP TLS/SSL","POP3 TLS/SSL","SOCKS proxy","Microsoft SQL server","MySQL server","Remote desktop protocol","VNC remote desktop"]

class Network:

    def __init__(self, ipAddress):
        self.ipAddress = ipaddress.ip_interface(ipAddress)
        self.ipNetwork = ipaddress.ip_network(str(self.ipAddress.network))
        self.csvColumns = "Date/Time,Host,Ping,TCP/19,TCP/21,TCP/22,TCP/23,TCP/25,TCP/80,TCP/110,TCP/137,TCP/138,TCP/139,TCP/389,TCP/445,TCP/902,TCP/903,TCP/993,TCP/995,TCP/1080,TCP/1433,TCP/3606,TCP/3389,TCP/5900\n"
        self.csvRows = ""
        self.csvColumnsExist = False
        self.ports = [19,21,22,23,25,80,110,137,138,139,143,179,389,43,445,902,903,993,995,1080,1433,3306,3389,5900]
    
    @staticmethod
    def is_valid_ip(ipAddress):
        valid = []

        try:
            valid = ipaddress.ip_interface(ipAddress)
        except ValueError:
            print(ipAddress + " is not valid")
        
        return valid
    
    def write_to_csv(self, fileName):
        csv = open(fileName, "a")

        if self.csvColumnsExist == False:
            csv.write(self.csvColumns)
        csv.write(self.csvRows)

        csv.close()

    def ping_network(self):       
        self.csvRows = ""

        for ip in self.ipNetwork:
            
            startTime = datetime.datetime.now().replace(microsecond=0)
            response = os.system("ping -c 1 -W 5 " + str(ip) + " > /dev/null")
            pinged = "no"
            self.csvRows += str(startTime) + "," + str(ip) + ","
        
            if response == 0:
                print("0 Connection accepted from ", str(ip))
                pinged = "yes"
            elif response == 1: 
                print("1 Timeout from ", str(ip))
                pinged = "timeout"
            else:
                print("2 Refused from ", str(ip))
                pinged = "no"
            
            self.csvRows += pinged + ","

            for index, port in enumerate(self.ports):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.002) 
                result = sock.connect_ex((str(ip),port))
        
                # SUCCESSFU
                if result == 0:
                    print ("Port: " + str(port) + " is open on " + str(ip))
                    self.csvRows += "Open"
                else:
                    print ("Port: " + str(port) + " is closed on " + str(ip))
                    self.csvRows += "Closed"
                sock.close()
        
                if index != 23:
                    self.csvRows +=","
                elif index == 23:
                    self.csvRows +="\n"

    
ipAddress = input("IP Address: ")
while not Network.is_valid_ip(ipAddress):
    ipAddress = input("IP Address: ")

network1 = Network(ipAddress)

network1.ping_network()
network1.write_to_csv("information.csv")

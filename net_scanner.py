import ipaddress  #Allows for IP address manipulation
import sys
import os 
import datetime
import csv 
import socket

ports = [19,21,22,23,25,80,110,137,138,139,143,179,389,43,445,902,903,993,995,1080,1433,3306,3389,5900]

def TCPConnect(ip):
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2) 
        result = sock.connect_ex((str(ip),port))
        
        # SUCCESSFU
        if result == 0:
            print ("Port: " + str(port) + " is open on " + str(ip))
        else:
            print ("Port: " + str(port) + " is closed on " + str(ip))
        sock.close()

def isValidIP(ip_address): 
    valid = []
    try:
        valid = ipaddress.ip_interface(ip_address)
    except ValueError:
        print("IP: ", ip_address, " is invalid.")
    return valid
    
ip_address = input("IP Address: ")
while not isValidIP(ip_address):
    ip_address = input("IP Address: ")

# Create an interface
ip_address = ipaddress.ip_interface(ip_address)

# Get a handle on network
network = ipaddress.ip_network(str(ip_address.network))

csv = open("information.csv", "a")
csv.write("Date/Time"+ "," + "Host" + "," + "Ping" + "\n")

for ip in network:
    response = os.system("ping -c 1 -W 5 " + str(ip) + " > /dev/null")
    pinged = "no"
    
    if response == 0:
        print("0 Connection accepted from ", str(ip))
        pinged = "yes"
        TCPConnect(ip)
    elif response == 1: 
        print("1 Timeout from ", str(ip))
    else:
        print("2 Refused from ", str(ip))
    
    csv.write(str(datetime.datetime.now().replace(microsecond=0)) + "," + str(ip) + "," + str(pinged)+"\n")

csv.close()

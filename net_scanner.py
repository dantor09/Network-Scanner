import ipaddress  #Allows for IP address manipulation
import sys
import os 
import datetime
import csv 

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
    elif response == 1: 
        print("1 Timeout from ", str(ip))
    else:
        print("2 Refused from ", str(ip))
    
    csv.write(str(datetime.datetime.now().replace(microsecond=0)) + "," + str(ip) + "," + str(pinged)+"\n")

csv.close()

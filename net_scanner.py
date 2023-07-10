import subprocess #allows for command line execution
import ipaddress  #Allows for IP address manipulation
import sys
import re
import os 
import datetime

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


ip_ping_response = []
ip_ping_timeout = []
ip_ping_refuse = []

#iterate through ip in network
for ip in network:
    response = os.system("ping -c 1 " + str(ip))

    if response == 0:
        print("0 Connection accepted from ", str(ip))
        ip_ping_response.append(ip)
    elif response == 1: 
        print("1 Timeout from ", str(ip))
        ip_ping_timeout.append(ip)
    else:
        print("2 Refused from ", str(ip))
        ip_ping_refuse.append(ip)
    print(datetime.datetime.now())



print(ip_ping_response)


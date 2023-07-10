import subprocess #allows for command line execution
import ipaddress  #Allows for IP address manipulation
import sys
import re

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


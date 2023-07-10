import subprocess #allows for command line execution
import ipaddress  #Allows for IP address manipulation
import sys
import re

def isValidIP(ip_address):
    ipv4_regex = r'^(\d){1,3}\.(\d){1,3}\.(\d){1,3}\.(\d){1,3}/(\d){1,2}$'
    valid = re.findall(ipv4_regex, ip_address)
    return valid

ip_address = input("IP Address: ")

while not isValidIP(ip_address):
    print(ip_address, " is invalid.")
    ip_address = input("IP Address: ")


import ipaddress  #Allows for IP address manipulation
import sys
import os 
import datetime
import csv 
import socket

ports = [19,21,22,23,25,80,110,137,138,139,143,179,389,43,445,902,903,993,995,1080,1433,3306,3389,5900]
protocol = ["Chargen","FTP","SSH","Telnet","SMTP","HTTP","POP3","NETBIOS","NETBIOS","NETBIOS","IMAP","BGP","LDAP","HTTPS","Microsoft directory services","VMware ESX","VMware ESX","IMAP TLS/SSL","POP3 TLS/SSL","SOCKS proxy","Microsoft SQL server","MySQL server","Remote desktop protocol","VNC remote desktop"]

def TCPConnect(ip):
    csv_rows =""
    for index, port in enumerate(ports):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2) 
        result = sock.connect_ex((str(ip),port))
        
        # SUCCESSFU
        if result == 0:
            print ("Port: " + str(port) + " is open on " + str(ip))
            csv_rows += "Open"
        else:
            print ("Port: " + str(port) + " is closed on " + str(ip))
            csv_rows += "Closed"
        sock.close()
        
        if index != 23:
            csv_rows+=","
    return csv_rows

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
    start_time = datetime.datetime.now().replace(microsecond=0)
    response = os.system("ping -c 1 -W 5 " + str(ip) + " > /dev/null")
    pinged = "no"
    csv_row = ""
        
    if response == 0:
        print("0 Connection accepted from ", str(ip))
        pinged = "yes"
        csv_row = TCPConnect(ip)
    elif response == 1: 
        print("1 Timeout from ", str(ip))
        for index in range(24):
            print(index)
            if index != 23:
                csv_row += "Closed,"
            else:
                csv_row += "Closed"
    else:
        print("2 Refused from ", str(ip))

        for index in range(24):
            print(index)
            if index != 23:
                csv_row += "Closed," 
            else:
                csv_row += "Closed"
    csv.write(str(start_time) + "," + str(ip) + "," + str(pinged)+ "," +csv_row + "\n")

csv.close()

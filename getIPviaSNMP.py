from pysnmp.hlapi import *
import re

""" Function to snmp into switch and get OS. This will require an snmp engine
    Will take a community string and ipaddress or hostname as arguments. If 2960 switch Function
    will return as a hex value which will need to be decoded for readability. If it is a nexus
    switch the return value is in acsii. Need to check via an if statement
    for testing purposes we are printing results.
"""

def findOS(community_string, hostname):

    get = getCmd(SnmpEngine(),
                 CommunityData(community_string),
                 UdpTransportTarget((hostname, 161)),
                 ContextData(),
                 ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))

    target = str(next(get))
    hexvalue = re.search('(?<= hexValue=\')..................', target)
    os = re.search('(?<=Cisco\s).....', target)

    if hexvalue:
        print(bytearray.fromhex(hexvalue.group()).decode())
    elif os:
        print(os.group())
    else:
        print("no os found")

if __name__=="__main__":

    community_string = input("community string")
    hostname = input("host address")
    findOS(community_string, hostname)



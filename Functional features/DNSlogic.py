import json
import paramiko
import sys
import ipaddress
import re
import os

Content = sys.argv[1]
my_DNS = sys.argv[2]
#Hyp_var="H2"
#Content="rfc_9"
def Edge_Server():


    with open("/home/root/DNS_mappings.txt") as f:
        y = json.loads(f.read())
        #print(y["RFC_9"])
    f1=0
    for key,value in y.items():
        if(key==Content):
            f1=1

    if(f1==0):
        print("File not published")
        os._exit(0)

    Edge_Servers = y[Content]                       #Input the logic of which RFC the customer wants to subscribe

    if ele in Edge_Servers:
        last_octet = ele.split(.)[-1]
        if int(last_octet)%2==1 and my_DNS=='10.0.0.254':
            Edge_IP_final=ele
        if int(last_octet)%2==1 and my_DNS=='11.0.0.254'
            Edge_IP_final=ele
    return(Edge_IP_final)


def get_Edge_IP():
    Edge_IP=Edge_Server()
    return(Edge_IP)

get_Edge_IP()

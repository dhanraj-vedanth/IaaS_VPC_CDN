import paramiko
import os
import subet_Gen
import getpass
import sys
import internetsouth


def Create_NS(NS_name):
    os.system("docker run --name "+NS_name+" --cap-add=NET_ADMIN -itd main-vm")
    print("docker run --name "+NS_name+" --cap-add=NET_ADMIN -itd main-vm")

def Create_RNS(NS_name):
    os.system("docker run --name "+NS_name+" --cap-add=NET_ADMIN -itd main-vm")
    print("docker run --name "+NS_name+" --cap-add=NET_ADMIN -itd main-vm")

def Internet_Create(NS_name): #subnet is 1.0.0.0/8
    #subnet="1.0.0.0"
    f=subet_Gen.start()
    print(f)
    internetsouth.internet_create_south(NS_name,f)


    #print("sh vxlan-create.sh " +NS_name+" "+"42 " +"ns_proj "+"vxlan0 " + f[0][1]+ " " + f[1][0] + " "+ "BR_NS" )
    #os.system("sh /home/ece792/project_codes/vxlan-create.sh " +NS_name+" "+"42 " +"ns_proj "+"vxlan0 " + f[0][1]+ " " + f[1][0] + " "+ "BR_NS")


def internet1(SG_var,flag):
    NS_name = SG_var
    Create_NS(NS_name)

    if(flag=="yes"):
        Internet_Create(NS_name)


def L3comm(subnet,subnet_var_list,Router,NS_name):
    f=subet_Gen.start()
    print(f)
    internetsouth.L3comm_south(subnet,subnet_var_list,Router,NS_name,f)
'''
flag="yes"
NS_name="Ram_int4"
Router="Router_int4"
subnet="11.0.0.0/24"
subnet_var_list=["11.0.0.0/24","12.0.0.0/24","13.0.0.0/24"]
#Create_NS(NS_name)
internet1(NS_name,flag)
Create_RNS(Router)
L3comm(subnet,subnet_var_list,Router,NS_name)
'''

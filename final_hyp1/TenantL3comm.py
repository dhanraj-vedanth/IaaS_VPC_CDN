import os
import ipaddress
import internetnL3comm_create
import sys


# a = input("Please input the number of subnets:\n")
# subnet_var_list=[]
# for i in range(0,int(a)):
#     b = input("Please input the subnet "+str(i+1)+"\n")
#     var_subnet=ipaddress.ip_network(b)
#     subnet_var_list.append(b)
# Tvar= sys.argv 
# a = sys.argv[2]
# b = sys.argv[3]


def internet(Tvar,subnet_var_list,flag):
    var_Router = "Router"+ str(Tvar)
    internetnL3comm_create.Create_RNS(var_Router)
    for i,val in enumerate(subnet_var_list):
                    #Tvar
        ''' Tenant<tenantno>SG<subnetno>'''
        SG_var = "Tenant" + str(Tvar) + "_SG_" + str(i+1) 
        # SG_var = "SG"+str(i+1)+Tvar
        internetnL3comm_create.internet1(SG_var, flag)
        print(SG_var)
        print(flag)
        print(var_Router)
        print(subnet_var_list[i])
        #internetnL3comm_create.internet1(SG_var, flag)
        internetnL3comm_create.L3comm(subnet_var_list[i],subnet_var_list, var_Router,SG_var)


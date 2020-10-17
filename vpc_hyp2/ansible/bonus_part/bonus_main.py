import re 
import os
import subprocess
from create_play import *


get_no_vms = input("Enter the number of vms to be spun: ")

vm_details = {}
vm_dets = {}

for x in range(int(get_no_vms)):
    connection_det = input("Give the connections you need (Internet/L3/L2) for VM number: " + str(x) + " separated by spaces: ")
    conn_det = connection_det.split()
    vm_details[x] = conn_det

for key,val in vm_details.items():
    temp_list = []
    for each in val:
        if each.lower() == 'internet':
            temp_list.append('ovs_nat')
        if each.lower() == 'l2':
            temp_list.append('ovs_l2')
        if each.lower() == 'l3':
            temp_list.append('ovs_l3')
    vm_dets[key] = temp_list

print("You have asked for the following")
print(vm_dets)

for k,v in vm_dets.items():
    if len(v) == 0:
        print("Invalid, exitting the code")
        exit(0)
    if len(v) == 1:
        int0 = 'default'
        int1 = str(v[0])
        print(int0,int1)
        #execute command
        vm_create1(int1,k)
        print(subprocess.getoutput("sudo ansible-playbook playbook" + str(k) + ".yml"))
        print("Please run the command: sudo virt-viewer autovm" + str(k) + " to complete installation")

    if len(v) == 2:
        int0 = 'default'
        int1 = str(v[0])
        int2 = str(v[1])
        print(int0,int1,int2)
        #execute command
        vm_create2(int1,int2,k)
        print(subprocess.getoutput("sudo ansible-playbook playbook" + str(k) + ".yml"))
        print("Please run the command: sudo virt-viewer autovm" + str(k) + " to complete installation")

    if len(v) == 3:
        int0 = 'default'
        int1 = str(v[0])
        int2 = str(v[1])
        int3 = str(v[2])
        print(int0,int1,int2,int3)
        #execute command
        vm_create3(int1,int2,int3,k)
        print(subprocess.getoutput("sudo ansible-playbook playbook" + str(k) + ".yml"))
        print("Please run the command: sudo virt-viewer autovm" + str(k) + " to complete installation")




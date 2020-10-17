import os
import sys


for i in range(10,50):
    for j in range(1,60):
            print(os.system("sudo virsh destroy tenant" + str(i) + "vm" + str(j)))
            print(os.system("sudo virsh undefine tenant" + str(i) + "vm" + str(j)))

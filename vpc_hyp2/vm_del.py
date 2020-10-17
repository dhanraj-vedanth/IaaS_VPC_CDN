import os
import sys


for i in range(1,50):
    for j in range(1,11):
        for x in range(1,4):
            print(os.system("sudo virsh destroy tenant" + str(i) + "vm" + str(j) + "_" + str(x)))
            print(os.system("sudo virsh undefine tenant" + str(i) + "vm" + str(j) + "_" + str(x)))

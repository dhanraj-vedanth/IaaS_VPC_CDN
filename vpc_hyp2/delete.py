import sys
import os


for i in range(1,90):
    for n in range(1,3):
        print(os.system("sudo ovs-vsctl del-br tenant" + str(i) + "br_" +str(n)))

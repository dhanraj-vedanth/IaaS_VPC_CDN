import os
import sys

for i in range(1,100):
    for x in range(1,3):
        print(os.system("sudo ip link del t" + str(i) + "_" + str(x) + "vx"))


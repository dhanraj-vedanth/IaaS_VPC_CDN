import os
import paramiko
import json
import subprocess

container_name = []
with open('/home/ece792/vpc/management/edge_input.json','r+') as reader:
    data = json.load(reader)
    container_name = data["Container_name"]


with open('/home/ece792/vpc/management/monitor.csv','w+') as w:
    w.write("STATUS, PID, STARTED_AT, MEMORY, SWAP, MGMT_IP\n")

    for each in container_name:
        output_arr = []

        output_arr.append(subprocess.getoutput('sudo docker inspect -f ' + '"{{ .State.Status }}" ' + str(each)))
        output_arr.append(subprocess.getoutput('sudo docker inspect -f ' + '"{{ .State.Pid }}" ' + str(each)))
        output_arr.append(subprocess.getoutput('sudo docker inspect -f ' + '"{{ .State.StartedAt }}" ' + str(each)))

        output_arr.append(subprocess.getoutput('sudo docker inspect -f ' + '"{{ .HostConfig.Memory }}" ' + str(each)))

        output_arr.append(subprocess.getoutput('sudo docker inspect -f ' + '"{{ .HostConfig.MemorySwap }}" ' + str(each)))

        output_arr.append(subprocess.getoutput('sudo docker inspect -f ' + '"{{ .NetworkSettings.IPAddress }}" ' + str(each)))
        lent = len(output_arr)
        for num,each in enumerate(output_arr):
            if num != lent -1:
                w.write(str(each))
                w.write(',')
            else:
                w.write(str(each))
        w.write('\n')



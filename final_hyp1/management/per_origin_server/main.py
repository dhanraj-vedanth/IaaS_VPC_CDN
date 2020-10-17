import os
import sys
import paramiko
import subprocess
import json

container_name = []
with open('./input_data.json','r+') as reader:
    data = json.load(reader)
    container_name = data["Container_name"]


to_pass = ' '.join(container_name)


ssh_client=paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname='192.168.122.195',username='root',password='hourglass')

print(to_pass)
print('docker stats --no-stream --format ' + '"table {{.Container}} {{.CPUPerc}} {{.MemUsage}}" ' + str(to_pass))
#input()
stdin,stdout,stderr=ssh_client.exec_command('docker stats --no-stream --format ' + '"table {{.Container}} {{.CPUPerc}} {{.MemUsage}}" ' + str(to_pass))

output = stdout.read()
#print(output)
exit_status = stdout.channel.recv_exit_status()          # Blocking call
if exit_status == 0:
    print("Grabbing info")
#    print ("Success-pt3!")
#    print(stderr)
else:
    print("Error", exit_status)

output_list = output.splitlines()
print("\n ***************************")
for each in output_list:
    print(each)
#output = subprocess.getouput('docker stats --no-stream --format ' + '"table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" ' + str(to_pass))


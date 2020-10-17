import paramiko
import json
import subprocess
import os


container_name = ''

with open('/home/ece792/vpc/management/origin_input.json','r+') as reader:
    data = json.load(reader)
    # print(data)
    container_name = data["Container_name"]


ip_to_ssh = subprocess.getoutput('sudo docker inspect -f ' + '"{{ .NetworkSettings.IPAddress }}" ' + str(container_name))
print(ip_to_ssh)
input()
ssh_client=paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ip_to_ssh,username='root',password='root')
stdin,stdout,stderr=ssh_client.exec_command("rm /etc/influxdb/influxdb.conf")
exit_status = stdout.channel.recv_exit_status()          # Blocking call
if exit_status == 0:
    print ("Successfully removed the influxdb.conf file!")
    print(stderr)
else:
    print("Error", exit_status)
    print(stderr)
ftp_client=ssh_client.open_sftp()
ftp_client.put('/home/ece792/vpc/management/influxdb.conf','/etc/influxdb/influxdb.conf')
ftp_client.close()
stdin,stdout,stderr=ssh_client.exec_command("sudo service influxd start")
exit_status = stdout.channel.recv_exit_status()          # Blocking call
if exit_status == 0:
    print ("Successfully created the new config file!")
    print(stderr)
else:
    print("Error", exit_status)
    print(stderr)
ftp_client=ssh_client.open_sftp()
print("Successfully started the influxdb service")



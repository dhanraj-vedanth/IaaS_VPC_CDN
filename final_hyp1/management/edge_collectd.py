import os
import paramiko
import json
import subprocess

container_name = []
with open('/home/ece792/vpc/management/edge_input.json','r+') as reader:
    data = json.load(reader)
    container_name = data["Container_name"]

'''*************NEW STUFF******************'''

for each in container_name:
    ip_to_ssh = subprocess.getoutput('sudo docker inspect -f ' + '"{{ .NetworkSettings.IPAddress }}" ' + str(each))
    print(ip_to_ssh)
    print(type(ip_to_ssh))
    ssh_client=paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip_to_ssh,username='root',password='root')
    stdin,stdout,stderr=ssh_client.exec_command("pwd")
    exit_status = stdout.channel.recv_exit_status()          # Blocking call
    if exit_status == 0:
        print ("Test da")
        print(stderr)
    else:
        print("Error", exit_status)
        print(stderr)
    stdin,stdout,stderr=ssh_client.exec_command("rm /etc/collectd/collectd.conf")
    exit_status = stdout.channel.recv_exit_status()          # Blocking call
    if exit_status == 0:
        print ("Successfully removed the collectd file!")
        print(stderr)
    else:
        print("Error", exit_status)
        print(stderr)
    ftp_client=ssh_client.open_sftp()
    ftp_client.put('/home/ece792/vpc/management/collectd.conf','/etc/collectd/collectd.conf')
    ftp_client.close()
    stdin,stdout,stderr=ssh_client.exec_command("sudo service collectd start")
    exit_status = stdout.channel.recv_exit_status()          # Blocking call
    if exit_status == 0:
        print ("Successfully removed the collectd file!")
        print(stderr)
    else:
        print("Error", exit_status)
        print(stderr)
    ftp_client=ssh_client.open_sftp()
    print("Successfully created the new config file")


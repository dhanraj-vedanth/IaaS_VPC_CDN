from netmiko import ConnectHandler
import os
import time
import paramiko

tenant_check = 11
each = 40


#domain_name = "tenant" + str(tenant_check) + "vm" + str(each)
#domain = {'device_type': "linux",'ip': "192.168.122.175", 'username': "root", 'password': "mesh@123"}
#net_connect1 = ConnectHandler(**domain)
#net_connect1.enable()
#print(net_connect1.send_command("pwd"))

ssh_client=paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname='192.168.122.175',username='root',password='mesh@123')
stdin,stdout,stderr=ssh_client.exec_command("pwd")

exit_status = stdout.channel.recv_exit_status()          # Blocking call
if exit_status == 0:
    print ("Success-pt1!")
    print(stderr)
else:
    print("Error", exit_status)
    print(stderr)



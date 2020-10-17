import os
import re
import sys
from netmiko import ConnectHandler
import ipaddress
import paramiko

root_cdn = '24.16.8.2/24'

def DNS_IP():
    os.system("ip addr | grep -A 3 \"eth0\" > /home/ip_text2.txt")
    f=open("/home/ip_text2.txt", "r+")
    for line in f:
        if re.search("inet", line):
            IP_eth0=line.split()[1]

    H_IP = ipaddress.ip_interface(IP_eth0)
    N_A = ipaddress.ip_network(H_IP, strict=False)
    print(N_A)
    if str(N_A) == "188.0.0.0/16":
        DNS_server = '10.0.0.254'
    elif str(N_A) == "189.0.0.0/16":
        DNS_server = '11.0.0.254'
    return(DNS_server)

def funcfeat1():
    my_dns_server_ip = DNS_IP()
    file_push=sys.argv[1]
    file_push_gen = "rfc_" + str(file_push)
    domain = {'device_type': "linux",'ip': str(my_dns_server_ip), 'username': "root", 'password': "root", 'secret': 'root'}
    net_connect = ConnectHandler(**domain)
    net_connect.enable()
    op1 = net_connect.send_command_timing("python3 /home/dns_pub.py " + str(file_push_gen)+" "+DNS_server)
    #op1 = net_connect.send_command_timing("python3 /home/dns_pub.py " + str(file_push_gen) + " " + str(my_ip_add))



    ES_list = []
    ES_list.append(op1.split('\n')[-1])
    ES_list.append(op1.split('\n')[-2])
    ES_list.append(root_cdn.split('/')[0])
    print(ES_list)


    #print(ES_list)
    '''paramiko for the two ips of op1'''

    for each_ip in ES_list:
        #print(each_ip)
        ssh_client=paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #print(each)
        ssh_client.connect(hostname=str(each_ip),username='root',password='root')
        ftp_client=ssh_client.open_sftp()
        #print("/home/cdn_data/" + str(file_push_gen) + ".txt,"+"/home/cdn_data/" + str(file_push_gen) + ".txt")
        a1="/home/cdn_data/" + str(file_push_gen) + ".txt"
        #print(a1)
        ftp_client.put(a1,a1)
        ftp_client.close()
        ssh_client.close()


funcfeat1()

import paramiko
import ipaddress
import re
import os
import netmiko
#import DNSlogic

ID = sys.argv[1]
Content = 'rfc_'+str(ID)


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


def filerec():
    DNS_server = DNS_server()
    #my_dns_server_ip = DNS_IP()
    file_push=sys.argv[1]
    file_push_gen = "rfc_" + str(file_push)
    domain = {'device_type': "linux",'ip': str(my_dns_server_ip), 'username': "root", 'password': "root", 'secret': 'root'}
    net_connect = ConnectHandler(**domain)
    net_connect.enable()
    op1 = net_connect.send_command_timing("python3 /home/DNSlogic.py " + str(file_push_gen)+" "+DNS_server)


    ssh_client=paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #Edge_IP=Edge_IP.split('/')[0]
    ssh_client.connect(hostname=Edge_IP,username='root',password='root')
    ftp_client=ssh_client.open_sftp()
    a1="/home/root/cdn_data/"+str(Content)+".txt"
    ftp_client.get(a1,a1)
    ftp_client.close()
    ssh_client.close()



filerec()

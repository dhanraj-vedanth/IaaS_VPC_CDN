import sys
import os
import ipaddress
from netmiko import ConnectHandler
import json
import paramiko
import json
import re

rfc_file = sys.argv[1]
my_Server = sys.argv[2]

f=open("/home/dict1.json",'r')
edge_dict=json.loads(f.read())

DNS_list = ['10.0.0.254','11.0.0.254']


def publisher(rfc_file):
    rfc_no = rfc_file.split('_')[1]
    print(rfc_no)
    origin_ip = '24.16.8.2/24'
    main_list = []


    if int(rfc_no) in range(1,11):
        #print("first subnet")
        for key,val in edge_dict.items():
            match=re.search('EdgeServer.*(\d)_.*',key)
            if match.group(1)=='1':
                main_list.append(val)
        main_list.append(origin_ip)

    if int(rfc_no) in range(11,21):
        for key,val in edge_dict.items():
            match=re.search('EdgeServer.*(\d)_.*',key)
            if match.group(1)=='2':
                main_list.append(val)
        main_list.append(origin_ip)

    if int(rfc_no) in range(21,31):
        for key,val in edge_dict.items():
            match=re.search('EdgeServer.*(\d)_.*',key)
            if match.group(1)=='3':
                main_list.append(val)
        main_list.append(origin_ip)

    return(main_list)


def dns_pub():
    subnet_list = publisher(rfc_file)
    print(subnet_list)

    '''
    DNS MAPPING LOGIC!!!!
    {"rfc_9":["10.0.0.253/24", "10.0.0.252/24"], "rfc_15":["20.0.0.253/24", "20.0.0.252/24"],
     "rfc_25":["30.0.0.253/24", "30.0.0.252/24"], "Main_Server":["24.16.10.8/24"]}

    '''
    data = {}
    data1={}
    with open('/home/DNS_mappings.txt') as json_file:
        data = json.load(json_file)
        #print(data)
        for key1,val1 in data.items():
            data1[key1] = val1
    #print(data1)
    #print(str(rfc_file))
    data1[str(rfc_file)] = subnet_list[:2]
    #print(data1)
    with open('/home/DNS_mappings.txt','w+') as json_writer:
        json.dump(data1, json_writer)
    #print(subnet_list)

    for each_ip in DNS_list:
        if(my_Server==each_ip):
            continue
        print(each_ip)
        ssh_client=paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=str(each_ip),username='root',password='root')
        ftp_client=ssh_client.open_sftp()
        ftp_client.put('/home/DNS_mappings.txt','/home/DNS_mappings.txt')
        ftp_client.close()

    return(subnet_list[:2])

    '''use subnet_list to send the data to others!!!'''


        #with open('/home/DNS_mappings.txt') as f:
        #ftp_client.putfo(f,'/home/DNS_mappings.txt',confirm=True)
        #ssh_client.close()



dns_pub()

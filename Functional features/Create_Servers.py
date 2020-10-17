import os
import sys
import json
import ipaddress
import paramiko

with open("/home/ece792/vpc/counter.txt", "r+") as w:
        each_line = w.readlines()
        for each in each_line:
            if "tenant_count" in each:
                count = each.split("=")[1]
                tenant_id = int(count) - 1

#tenant_id=138
br_1 = "tenant"+str(tenant_id)+"br_1"
br_2 = "tenant"+str(tenant_id)+"br_2"
br_3 = "tenant"+str(tenant_id)+"br_3"

#container_name ="T_119_E2"
#ip_addr = "12.0.0.254"

def CreateBrokerServers():
    with open("/home/ece792/vpc/subnets.txt") as f:
        lines = f.readlines()
        print(lines)
    i=1
    Broker_dict={}
    BrokerIP=[]
    for each in lines[:2]:
        ip_nw = str(each.split('\n')[0])
        my_ip = ipaddress.ip_interface(ip_nw)
        temp = ipaddress.ip_network(my_ip, strict=False)
        IP_list = []

        for ele in temp.hosts():
            IP_list.append(ele)

        Broker_dict["Brokerserver" + str(i)] = str(IP_list[-1])
        BrokerIP.append(str(IP_list[-1]))

        i+=1
    json1= json.dumps(Broker_dict)
    f = open("/home/ece792/vpc/dict.json","w")
    f.write(json1)
    f.close()

    #func_createcont(br_1,"Brokerserver1",BrokerIP[0])

    ssh_client=paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname='192.168.122.175',username='root',password='mesh@123')

    print("python3 /home/ece792/vpc/Createservers.py " +br_2 + " Brokerserver2 "+BrokerIP[0])
    stdin,stdout,stderr=ssh_client.exec_command("python3 /home/ece792/vpc/Createservers.py " +br_2 + " Brokerserver2 "+BrokerIP[0] ,get_pty=True)
    exit_status = stdout.channel.recv_exit_status()          # Blocking call
    if exit_status == 0:
        print ("Success-pt3!")
        print(stderr)
    else:
        print("Error", exit_status)
        print(stderr)



def func_createcont(br,r,IP):
    print("\nMaking containers "+r)
    print("sudo docker run -itd --cap-add=NET_ADMIN --name "+r+" main-vm")
    os.system("sudo docker run -itd --cap-add=NET_ADMIN --name "+r+" main-vm")
    print("ovs-docker add-port "+br+" brock "+r)
    os.system("ovs-docker add-port "+br+" brock "+r)
    print("sudo docker exec -it "+r+" ip route del default")
    os.system("sudo docker exec -it "+r+" ip route del default")
    print("sudo docker exec -it "+r+" dhclient brock")
    os.system("sudo docker exec -it "+r+" dhclient brock")

    print("sudo docker exec -it "+r+" ip addr add "+IP+"/24 dev brock")
    os.system("sudo docker exec -it "+r+" ip addr add "+IP+"/24 dev brock")





CreateBrokerServers()

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
                tenant_id = int(count)

#tenant_id=138
br_list=[]
br_1 = "tenant"+str(tenant_id)+"br_1"
br_2 = "tenant"+str(tenant_id)+"br_2"
br_3 = "tenant"+str(tenant_id)+"br_3"
br_list.append(br_1)
br_list.append(br_2)
br_list.append(br_3)

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

        Broker_dict["Brokerserver"+str(tenant_id)+"-" + str(i)] = str(IP_list[-1])
        BrokerIP.append(str(IP_list[-1]))

        i+=1
    json1= json.dumps(Broker_dict)
    f = open("/home/ece792/vpc/dict.json","w")
    f.write(json1)
    f.close()

    func_createcont(br_1,"Brokerserver"+str(tenant_id)+"-" +"1",BrokerIP[0])

    ssh_client=paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname='192.168.122.175',username='root',password='mesh@123')

    print("python3 /home/ece792/vpc/Createservers.py " +br_2 + " Brokerserver"+str(tenant_id)+"-" +"2 "+BrokerIP[0])

    stdin,stdout,stderr=ssh_client.exec_command("python3 /home/ece792/vpc/Createservers.py " +br_2 + " Brokerserver"+str(tenant_id)+"-" +"2 "+BrokerIP[1] ,get_pty=True)
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


def Edgeservers():
    with open('ServerCreation.txt', 'r') as in_file:
        in_dict = json.loads(in_file.read())
        c=[]
        c1 = in_dict["No of edge servers in Location 1 for RFC range 1-10"]
        c2 = in_dict["No of edge servers in Location 1 for RFC range 11-20"]
        c3 = in_dict["No of edge servers in Location 1 for RFC range 21-30"]
        c.append(c1)
        c.append(c2)
        c.append(c3)

        d1 = in_dict["No of edge servers in Location 2 for RFC range 1-10"]
        d2 = in_dict["No of edge servers in Location 2 for RFC range 11-20"]
        d3 = in_dict["No of edge servers in Location 2 for RFC range 21-30"]

    print("Creating edge servers in Location 1")
    with open("/home/ece792/vpc/subnets.txt") as f:
        lines = f.readlines()
        print(lines)

    Edge_dict={}
    EdgeIP=[]
    j=1

    for each in lines:
        #var_range = 'c'+str(j)
        if(len(c)<j):
            break
        for i in range(c[j-1]):
            ip_nw = str(each.split('\n')[0])
            my_ip = ipaddress.ip_interface(ip_nw)
            temp = ipaddress.ip_network(my_ip, strict=False)
            IP_list = []

            for ele in temp.hosts():
                IP_list.append(ele)

            Edge_dict["EdgeServer"+str(tenant_id)+"-" + str(j)+"_"+str(i+1)] = str(IP_list[-2-i*2])
            EdgeIP.append(str(IP_list[-2-i*2]))



            func_createcont(br_list[j-1],"EdgeServer"+str(tenant_id)+"-" + str(j)+"_"+str(i+1),str(IP_list[-2-i*2]))
        j+=1
    json2= json.dumps(Edge_dict)
    f = open("/home/ece792/vpc/dict1.json","w")
    f.write(json2)
    f.close()

def Edgeserversa():
    with open('/home/ece792/vpc/ServerCreation.txt', 'r') as in_file:
        in_dict = json.loads(in_file.read())
        d=[]
        #c1 = in_dict["No of edge servers in Location 1 for RFC range 1-10"]
        #c2 = in_dict["No of edge servers in Location 1 for RFC range 11-20"]
        #c3 = in_dict["No of edge servers in Location 1 for RFC range 21-30"]

        d1 = in_dict["No of edge servers in Location 2 for RFC range 1-10"]
        d2 = in_dict["No of edge servers in Location 2 for RFC range 11-20"]
        d3 = in_dict["No of edge servers in Location 2 for RFC range 21-30"]
        d.append(d1)
        d.append(d2)
        d.append(d3)


    print("Creating edge servers in Location 2")
    with open("/home/ece792/vpc/subnets.txt") as f:
        lines = f.readlines()
        print(lines)

    Edge_dict={}
    EdgeIP=[]
    j=1

    for each in lines:
        #var_range = 'c'+str(j)
        if(len(d)<j):
            break
        for i in range(d[j-1]):
            ip_nw = str(each.split('\n')[0])
            my_ip = ipaddress.ip_interface(ip_nw)
            temp = ipaddress.ip_network(my_ip, strict=False)
            IP_list = []

            for ele in temp.hosts():
                IP_list.append(ele)

            Edge_dict["EdgeServer" +str(tenant_id)+"-"+ str(j)+"_a"+str(i+1)] = str(IP_list[-1-(i+1)*2])
            EdgeIP.append(str(IP_list[-2-i*2]))



            ssh_client=paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname='192.168.122.175',username='root',password='mesh@123')

            print("python3 /home/ece792/vpc/Createservers.py " +br_list[j-1] + " EdgeServer"+str(tenant_id)+"-" + str(j)+"_a"+str(i+1)+" "+str(IP_list[-1-(i+1)*2]))
            stdin,stdout,stderr=ssh_client.exec_command("python3 /home/ece792/vpc/Createservers.py " +br_list[j-1] + " EdgeServer"+str(tenant_id) + str(j)+"_a"+str(i+1)+" "+str(IP_list[-1-(i+1)*2]),get_pty=True)
            exit_status = stdout.channel.recv_exit_status()          # Blocking call
            if exit_status == 0:
                print ("Success-pt3!")
                print(stderr)
            else:
                print("Error", exit_status)
                print(stderr)
            
        j+=1
    #json2= json.dumps(Edge_dict)
    f = open("/home/ece792/vpc/dict1.json","r")
    dict_out = json.loads(f.read())
    for key,val in Edge_dict.items():
        dict_out[key]=val
    f.close()
    json2= json.dumps(dict_out)
    f = open("/home/ece792/vpc/dict1.json","w")
    f.write(json2)
    f.close()





CreateBrokerServers()
Edgeservers()
Edgeserversa()

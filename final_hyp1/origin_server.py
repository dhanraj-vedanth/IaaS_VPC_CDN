import os
import sys
import paramiko
import json



ip_addr = []
tenant_check = sys.argv[1]
container_name = "Origin{}".format(tenant_check)
Router_name = 'Router{}'.format(tenant_check)
# sg_name = []

#inputs
'''
Router_name = "Router119"
container_name ="Origin119"
ip_addr = ["12.0.0.0/24","11.0.0.0/24"] #subnet ips
'''

with open('/home/ece792/vpc/origin_input.json','r+') as reader:
    data = json.load(reader)

    # print(data)
    ip_addr = data["Subnet_IPs"]

print("*******CREATING THE FOLLOWING***************")
print("*  IP Address: {}".format(ip_addr))
print("*******************************************")

input()

def func_createcont(r):
        print("\nMaking containers "+r)
        print("sudo docker run -itd --cap-add=NET_ADMIN --name "+r+" dv_img")
        os.system("sudo docker run --name "+r+" --cap-add=NET_ADMIN -itd main-vm")

def func_createvethpair(vp1,vp2):
        print("Creating vethpairs")
        print("sudo ip link add "+vp1+" type veth peer name "+vp2)
        os.system("sudo ip link add "+vp1+" type veth peer name "+vp2)
        print("sudo ip link set {} up".format(vp1))
        os.system("sudo ip link set {} up".format(vp1))
        print("sudo ip link set {} up".format(vp2))
        os.system("sudo ip link set {} up".format(vp2))

def func_attachpid(vp,ns,c='0'):
        print("Attaching veth pairs")
        if c=='1':
                print("sudo docker inspect -f {{.State.Pid}} "+ns)     #pid addigning
                pid=os.popen("sudo docker inspect -f {{.State.Pid}} "+ns).read()
                print("sudo ip link set "+vp+" netns pid")
                os.system("sudo ip link set "+vp+" netns "+str(int(pid)))
                print("sudo docker exec "+ns+" ip link set "+vp+" up")
                os.system("sudo docker exec "+ns+" ip link set "+vp+" up")
        else:
                print("sudo ip link set "+vp+" netns "+ns)
                os.system("sudo ip link set "+vp+" netns "+ns)
                print("sudo ip netns exec "+ns+" ip link set "+vp+" up")
                os.system("sudo ip netns exec "+ns+" ip link set "+vp+" up")

def func_giveip(cont,ip,dev,c='0'):
        print("Assigning IPs")
        if c=='1':
                print("sudo ip netns exec "+cont+" ip addr add "+ip+" dev "+dev )
                os.system("sudo ip netns exec "+cont+" ip addr add "+ip+" dev "+dev)
        else:
                print("sudo docker exec "+cont+" ip addr add "+ip+" dev "+dev)
                os.system("sudo docker exec "+cont+" ip addr add "+ip+" dev "+dev)


def caller_fn():
        func_createcont(container_name)
        func_createvethpair("o"+container_name,container_name+"r")
        func_attachpid(container_name+"r",container_name,"1")
        func_attachpid("o"+container_name,Router_name,"1")
        func_giveip(container_name,"24.16.8.2/24",container_name+"r")
        func_giveip(Router_name,"24.16.8.1/24","o"+container_name)
        #adding routes
        i=len(ip_addr)

        for s in range(i):
                print("sudo docker exec {} ip route add ".format(container_name)+ip_addr[s]+" dev "+container_name+"r via 24.16.8.1")
                os.system("sudo docker exec {} ip route add ".format(container_name)+ip_addr[s]+" dev "+container_name+"r via 24.16.8.1")

caller_fn()




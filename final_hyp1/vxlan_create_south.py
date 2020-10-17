import paramiko
import os
import subnet_gen
import getpass
import time
import sys



def vxlan_create_south(NS_name,f):
    print("ip link add ns_proj type veth peer name "+NS_name )
    os.system("ip link add ns_proj type veth peer name "+NS_name)

    pid=os.popen('docker inspect -f \'{{.State.Pid}}\' ' +NS_name).read()
    print(pid)
    pid = pid.split('\n')[0]
    print("ip link set netns "+pid+" dev ns_proj")
    os.system("ip link set netns "+pid+" dev ns_proj")

    #print("ip link set ns_proj netns "+NS_name)
    #os.system("ip link set ns_proj netns "+NS_name)

    #time.sleep(3)

    pid=os.popen('docker inspect -f \'{{.State.Pid}}\' ' +"proj1").read()
    print(pid)
    pid = pid.split('\n')[0]
    print("ip link set netns "+pid+" dev "+ NS_name)
    os.system("ip link set netns "+pid+" dev "+ NS_name)

    #print("ip link set "+NS_name +" netns proj1")
    #os.system("ip link set "+NS_name+" netns proj1")

    print("docker exec -it "+NS_name+" brctl addbr BR_NS")
    os.system("docker exec -it "+NS_name+" brctl addbr BR_NS")
    os.system("docker exec -it "+NS_name+" ip link set BR_NS up")
    print("docker exec -it "+NS_name+" ip link set ns_proj up")
    os.system("docker exec -it "+NS_name+" ip link set ns_proj up")

    print("docker exec -it proj1 "+"ip link set "+ NS_name + " up")
    os.system("docker exec -it proj1 "+"ip link set "+ NS_name + " up")


    print("docker exec -it "+NS_name+" ip addr add " +f[0][1] +"/30"+" dev " + "ns_proj")
    os.system("docker exec -it "+NS_name+" ip addr add " +f[0][1] +"/30"+" dev " + "ns_proj")

    print("docker exec -it proj1 "+"ip addr add " +f[0][0] +"/30"+" dev " +NS_name)
    os.system("docker exec -it proj1 "+"ip addr add " +f[0][0] +"/30"+" dev " +NS_name)


    print("sh vxlan-create.sh " +NS_name+" "+"42 " +"ns_proj "+"vxlan0 " + f[1][1]+ " " + f[0][0] + " "+ "BR_NS" )
    os.system("sh /home/ece792/vpc/vxlan-create.sh " +NS_name+" "+"42 " +"ns_proj "+"vxlan0 " + f[1][1]+ " " + f[0][0] + " "+ "BR_NS")

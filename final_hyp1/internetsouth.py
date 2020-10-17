import paramiko
import os
import getpass
import sys



def internet_create_south(NS_name,f):

    print("ip link add ns_proj type veth peer name "+NS_name )
    os.system("ip link add ns_proj type veth peer name "+NS_name)

    pid=os.popen('docker inspect -f \'{{.State.Pid}}\' ' +NS_name).read()
    print(pid)
    pid = pid.split('\n')[0]
    print("ip link set netns "+pid+" dev ns_proj")
    os.system("ip link set netns "+pid+" dev ns_proj")


    pid=os.popen('docker inspect -f \'{{.State.Pid}}\' ' +"proj_internet").read()
    print(pid)
    pid = pid.split('\n')[0]
    print("ip link set netns "+pid+" dev "+ NS_name)
    os.system("ip link set netns "+pid+" dev "+ NS_name)


    #print("docker exec -it "+NS_name+" brctl addbr BR_NS")
    #os.system("docker exec -it "+NS_name+" brctl addbr BR_NS")
    #os.system("docker exec -it "+NS_name+" ip link set BR_NS up")
    print("docker exec -it "+NS_name+" ip link set ns_proj up")
    os.system("docker exec -it "+NS_name+" ip link set ns_proj up")

    print("docker exec -it proj_internet "+"ip link set "+ NS_name + " up")
    os.system("docker exec -it proj_internet "+"ip link set "+ NS_name + " up")


    print("docker exec -it "+NS_name+" ip addr add " +f[0][1] +"/30"+" dev " + "ns_proj")
    os.system("docker exec -it "+NS_name+" ip addr add " +f[0][1] +"/30"+" dev " + "ns_proj")

    print("docker exec -it proj_internet "+"ip addr add " +f[0][0] +"/30"+" dev " +NS_name)
    os.system("docker exec -it proj_internet "+"ip addr add " +f[0][0] +"/30"+" dev " +NS_name)

    print("docker exec -it "+NS_name+" ip route del default via 188.0.0.1")
    os.system("docker exec -it "+NS_name+" ip route del default via 188.0.0.1")



    print("docker exec -it "+NS_name+" ip route add default via " +f[0][0])
    os.system("docker exec -it "+NS_name+" ip route add default via " +f[0][0])

    print("docker exec -it "+NS_name+" iptables -t nat -A POSTROUTING -s 0.0.0.0/0 -j MASQUERADE -o ns_proj")
    os.system("docker exec -it "+NS_name+" iptables -t nat -A POSTROUTING -s 0.0.0.0/0 -j MASQUERADE -o ns_proj")





def L3comm_south(subnet,subnet_var_list,Router,NS_name,f):


    print("ip link add ns_proj1 type veth peer name "+NS_name )
    os.system("ip link add ns_proj1 type veth peer name "+NS_name)

    pid=os.popen('docker inspect -f \'{{.State.Pid}}\' ' +NS_name).read()
    print(pid)
    pid = pid.split('\n')[0]
    print("ip link set netns "+pid+" dev ns_proj1")
    os.system("ip link set netns "+pid+" dev ns_proj1")


    pid=os.popen('docker inspect -f \'{{.State.Pid}}\' ' +Router).read()
    print(pid)
    pid = pid.split('\n')[0]
    print("ip link set netns "+pid+" dev "+ NS_name)
    os.system("ip link set netns "+pid+" dev "+ NS_name)


    #print("docker exec -it "+NS_name+" brctl addbr BR_NS")
    #os.system("docker exec -it "+NS_name+" brctl addbr BR_NS")
    #os.system("docker exec -it "+NS_name+" ip link set BR_NS up")

    
    print("docker exec -it "+Router+" ip route del default via 188.0.0.1")
    os.system("docker exec -it "+Router+" ip route del default via 188.0.0.1")

    print("docker exec -it "+NS_name+" ip link set ns_proj1 up")
    os.system("docker exec -it "+NS_name+" ip link set ns_proj1 up")

    print("docker exec -it " +Router +" ip link set "+ NS_name + " up")
    os.system("docker exec -it " +Router +" ip link set "+ NS_name + " up")


    print("docker exec -it "+NS_name+" ip addr add " +f[0][1] +"/30"+" dev " + "ns_proj1")
    os.system("docker exec -it "+NS_name+" ip addr add " +f[0][1] +"/30"+" dev " + "ns_proj1")

    print("docker exec -it "+ Router +" ip addr add " +f[0][0] +"/30"+" dev " +NS_name)
    os.system("docker exec -it "+ Router +" ip addr add " +f[0][0] +"/30"+" dev " +NS_name)


    print("docker exec -it "+Router+" ip route add " +subnet+" via " +f[0][1])
    os.system("docker exec -it "+Router+" ip route add " +subnet+" via " +f[0][1])

    for ele in subnet_var_list:
        if(ele==subnet):
            continue
        else:
            print("docker exec -it "+NS_name+" ip route add " +ele+" via " +f[0][0])
            os.system("docker exec -it "+NS_name+" ip route add " +ele+" via " +f[0][0])
    print("docker exec -it "+NS_name+" ip route add 24.16.8.0/24 via "+f[0][0])
    os.system("docker exec -it "+NS_name+" ip route add 24.16.8.0/24 via "+f[0][0])

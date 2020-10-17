import os
import sys
import json
import ipaddress
import paramiko

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

br=sys.argv[1]
r=sys.argv[2]
IP=sys.argv[3]
func_createcont(br,r,IP)

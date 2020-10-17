import os
import sys

# br_name = sys.argv[1]
# container_name = sys.argv[2]
# ip_addr = sys.argv[3]

Router_name = "Router118"
container_name ="Origin118"
ip_addr = ["12.0.0.0","11.0.0.0"] #subnet ips
sg_name=["Tenant118_SG_1","Tenant118_SG_2"] 

def func_createcont(r):
        print("\nMaking containers "+r)
        print("sudo docker run -itd --cap-add=NET_ADMIN --name "+r+" dv_img")
        #os.system("sudo docker run -itd --cap-add=NET_ADMIN --name "+r+" edge1")

def func_createvethpair(vp1,vp2):
        print("Creating vethpairs")
        print("sudo ip link add "+vp1+" type veth peer name "+vp2)
        #os.system("sudo ip link add "+vp1+" type veth peer name "+vp2)
        print("sudo ip link set {} up".format(vp1))
        #os.system("sudo ip link set {} up".format(vp1))
        print("sudo ip link set {} up".format(vp2))
        #os.system("sudo ip link set {} up".format(vp2))

def func_attachpid(vp,ns):
        print("Attaching veth pairs")
        print("sudo docker inspect -f {{.State.Pid}} "+ns)     #pid addigning
        #pid=os.popen("sudo docker inspect -f {{.State.Pid}} "+ns).read()
        print("sudo ip link set "+vp+" netns pid")
        #os.system("sudo ip link set "+vp+" netns "+str(int(pid)))
        print("sudo docker exec "+ns+" ip link set "+vp+" up")
        #os.system("sudo docker exec "+ns+" ip link set "+vp+" up")

def func_giveip(cont,ip,dev):
        print("Assigning IPs")
        print("sudo docker exec "+cont+" ip addr add "+ip+"/24 dev "+dev)
        #os.system("sudo docker exec "+cont+" ip addr add "+ip+"/24 dev "+dev)

func_createcont(container_name)
func_createvethpair("o"+container_name,container_name+"r")
func_attachpid(container_name+"r",container_name)
func_attachpid("o"+container_name,Router_name)
func_giveip(container_name,"200.10.20.30",container_name+"r")
func_giveip(Router_name,"200.10.20.29","o"+container_name)
#changing default routes
i=len(ip_addr)

for s in range(i):
        print("sudo docker exec {} ip route add ".format(container_name)+ip_addr[s]+"/24 dev "+container_name+"r via 200.10.20.29")
        #os.system("sudo docker exec {} ip route add ".format(container_name)+ip_addr[s]+"/24 dev "+container_name+"r via 200.10.20.29")
#adding routes in subnet gateway
for sg in sg_name:
        print("sudo ip netns exec "+sg+" ip route add 200.10.20.0/24 dev ns_proj1")
        os.system("sudo ip netns exec "+sg+" ip route add 200.10.20.0/24 dev ns_proj1")

#adding influxdb part
#add influxdb part


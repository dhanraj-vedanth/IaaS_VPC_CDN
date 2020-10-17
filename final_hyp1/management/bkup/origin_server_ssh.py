import os
import sys
import json
import paramiko

Router_name = ''
container_name = ''
ip_addr = []
# sg_name = []

#inputs
'''
Router_name = "Router119"
container_name ="Origin119"
ip_addr = ["12.0.0.0","11.0.0.0"] #subnet ips
sg_name=["Tenant119_SG_2","Tenant119_SG_1"]
'''

with open('origin_input.json','r+') as reader:
    data = json.load(reader)

    # print(data)
    Router_name = data["Router_name"]
    container_name = data["Container_name"]
    ip_addr = data["Subnet_IPs"]

print("*******CREATING THE FOLLOWING***************")
print("*  Router Name: {}".format(Router_name))
print("*  Container Name: {}".format(container_name))
print("*  IP Address: {}".format(ip_addr))
print("*******************************************")

input()


def func_createcont(r):
        print("\nMaking containers "+r)
        print("sudo docker run -itd --cap-add=NET_ADMIN --name "+r+" dv_img")
        os.system("sudo docker run -itd --cap-add=NET_ADMIN --name "+r+" edge1")

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
                print("sudo ip netns exec "+cont+" ip addr add "+ip+"/24 dev "+dev )
                os.system("sudo ip netns exec "+cont+" ip addr add "+ip+"/24 dev "+dev)
        else:
                print("sudo docker exec "+cont+" ip addr add "+ip+"/24 dev "+dev)
                os.system("sudo docker exec "+cont+" ip addr add "+ip+"/24 dev "+dev)

func_createcont(container_name)
func_createvethpair("o"+container_name,container_name+"r")
func_attachpid(container_name+"r",container_name,"1")
func_attachpid("o"+container_name,Router_name,"1")
func_giveip(container_name,"200.10.20.30",container_name+"r")
func_giveip(Router_name,"200.10.20.29","o"+container_name)
#adding routes
i=len(ip_addr)

for s in range(i):
        print("sudo docker exec {} ip route add ".format(container_name)+ip_addr[s]+"/24 dev "+container_name+"r via 200.10.20.29")
        os.system("sudo docker exec {} ip route add ".format(container_name)+ip_addr[s]+"/24 dev "+container_name+"r via 200.10.20.29")

#adding routes in subnet gateway
# for sg in sg_name:
#         print("sudo ip netns exec "+sg+" ip route add 200.10.20.0/24 dev ns_proj1")
#         os.system("sudo ip netns exec "+sg+" ip route add 200.10.20.0/24 dev ns_proj1")

''' NEW STUFF '''

ip_to_ssh = os.system('sudo docker inspect -f "{{ .NetworkSettings.IPAddress }}" {}'.format(container_name))
ssh_client=paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ip_to_ssh,username='root',password='root')
stdin,stdout,stderr=ssh_client.exec_command("rm /etc/influxdb/influxdb.conf")
exit_status = stdout.channel.recv_exit_status()          # Blocking call
if exit_status == 0:
    print ("Successfully removed the influxdb.conf file!")
    print(stderr)
else:
    print("Error", exit_status)
    print(stderr)
ftp_client=ssh_client.open_sftp()
ftp_client.put('/home/vpc/management/influxdb.conf','/etc/influxdb/influxdb.conf')
ftp_client.close()
stdin,stdout,stderr=ssh_client.exec_command("sudo service influxd start")
exit_status = stdout.channel.recv_exit_status()          # Blocking call
if exit_status == 0:
    print ("Successfully removed the influxdb.conf file!")
    print(stderr)
else:
    print("Error", exit_status)
    print(stderr)
ftp_client=ssh_client.open_sftp()
print("Successfully created the new config file")

import os
import sys
import json
import paramiko 

br_name = ''
container_name = ''
ip_addr = ''

with open('edge_input.json','r+') as reader:
    data = json.load(reader)

    # print(data)
    br_name = data["Bridge_name"]
    container_name = data["Container_name"]
    ip_addr = data["Container_ip"]

print("*******CREATING THE FOLLOWING***************")
print("*  Bridge Name: {}".format(br_name))
print("*  Container Name: {}".format(container_name))
print("*  IP Address: {}".format(ip_addr))
print("*******************************************")


ip_net=ip_addr[-(len(ip_addr)):-3]

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

def func_giveip(cont,ip,dev):
        print("Assigning IPs")
        print("sudo ip netns exec "+cont+" ip addr add "+ip+"/24 dev "+dev )
        os.system("sudo docker exec "+cont+" ip addr add "+ip+"/24 dev "+dev)

def func_attachpid(vp,ns,c='0'):
        print("Attaching veth pairs")
        if c=='1':
                print("sudo docker inspect -f {{.State.Pid}} "+ns)     #pid addigning
                pid=os.popen("sudo docker inspect -f {{.State.Pid}} "+ns).read()
                print("sudo ip link set "+vp+" netns pid")
                os.system("sudo ip link set "+vp+" netns "+str(int(pid)))
                print("sudo docker exec "+ns+" ip link set "+vp+" up" )
                os.system("sudo docker exec "+ns+" ip link set "+vp+" up")
        else:
                print("sudo ovs-vsctl add-port {} {}".format(ns,vp))
                os.system("sudo ovs-vsctl add-port {} {}".format(ns,vp))

func_createcont(container_name)
func_createvethpair("e"+container_name,container_name+"b")
func_attachpid(container_name+"b",container_name,"1")
func_attachpid("e"+container_name,br_name)
func_giveip(container_name,ip_addr,container_name+"b")
#changing default routes
print("sudo docker exec {} ip route del default via 188.0.0.1 ".format(container_name))
os.system("sudo docker exec {} ip route del default via 188.0.0.1 ".format(container_name))
print("sudo docker exec {} ip route add default via ".format(container_name)+ip_net+"1")
os.system("sudo docker exec {} ip route add default via ".format(container_name)+ip_net+"1")


'''*************NEW STUFF******************'''
ip_to_ssh = os.system('sudo docker inspect -f "{{ .NetworkSettings.IPAddress }}" {}'.format(container_name))
ssh_client=paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ip_to_ssh,username='root',password='root')
stdin,stdout,stderr=ssh_client.exec_command("rm /etc/collectd/collectd.conf")
exit_status = stdout.channel.recv_exit_status()          # Blocking call
if exit_status == 0:
    print ("Successfully removed the collectd file!")
    print(stderr)
else:
    print("Error", exit_status)
    print(stderr)
ftp_client=ssh_client.open_sftp()
ftp_client.put('/home/vpc/management/collectd.conf','/etc/collectd/collectd.conf')
ftp_client.close()
stdin,stdout,stderr=ssh_client.exec_command("sudo service collectd start")
exit_status = stdout.channel.recv_exit_status()          # Blocking call
if exit_status == 0:
    print ("Successfully removed the collectd file!")
    print(stderr)
else:
    print("Error", exit_status)
    print(stderr)
ftp_client=ssh_client.open_sftp()
print("Successfully created the new config file")

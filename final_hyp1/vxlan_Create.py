import paramiko
import os
import subnet_gen
import getpass
import time
import sys
import vxlan_create_south


# f=open("/home/ece792/project_codes/varfile.txt","r+")
# ns_var = f.readline().split('\n')
# NS_name = "NS_proj"+ns_var[0]
# NS_name = sys.argv[1]

'''
with open("/home/ece792/project_codes/varfile.txt", "r") as f:
    lines = f.readlines()
with open("/home/ece792/project_codes/varfile.txt", "w") as f:
    for line in lines:
        if line.strip("\n") != ns_var[0]:
            f.write(line)
'''



def Create_NS(NS_name):
    os.system("docker run --name "+NS_name+" --cap-add=NET_ADMIN -itd main-vm")
    print("docker run --name "+NS_name+" --cap-add=NET_ADMIN -itd main-vm")


def VXLAN_Create(NS_name):
    f=subnet_gen.start()

    mg1=f[0][0].split('.')
    mg2=f[0][1].split('.')
    mg3=str(int(mg1[2])+ 128)
    mg4=str(int(mg2[2])+ 128)

    lista=[]

    mg5=mg1[0]+"."+mg1[1]+"."+mg3+"."+mg1[3]
    mg6=mg2[0]+"."+mg1[1]+"."+mg4+"."+mg2[3]

    lista.append(mg5)
    lista.append(mg6)

    f.append(lista)


    print(f)

    vxlan_create_south.vxlan_create_south(NS_name,f)

    ssh_client=paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname='192.168.122.175',username='root',password='mesh@123')
    print("python3 /home/ece792/project_codes/vxlan_Create.py " + NS_name + " " + f[0][0]+ " "+ f[0][1]+ " " + f[1][0]+" "+f[1][1])
    stdin,stdout,stderr=ssh_client.exec_command("python3 /home/ece792/project_codes/vxlan_Create.py " + NS_name + " " + f[0][0]+ " "+ f[0][1]+ " " + f[1][0]+" "+f[1][1], get_pty=True)
    print(stdout)
    exit_status = stdout.channel.recv_exit_status()          # Blocking call
    if exit_status == 0:
        print ("File Deleted")
        print(stderr)
    else:
        print("Error", exit_status)
        print(stderr)


# n=input("How many VMs do you want to create?\n")
#Create_NS("rama101")
#VXLAN_Create("rama101")

def multicreate(NS_name):

    VXLAN_Create(NS_name)


        #client.close()

###
'''
else:
   # print("Meh")
    ssh_client=paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname='192.168.122.195',username='root',password='hourglass')
    ftp_client=ssh_client.open_sftp()
    ftp_client.put('/home/ece792/project_codes/varfile.txt','/home/ece792/project_codes/varfile.txt')
   # stdin,stdout,stderr=ssh_client.exec_command("scp ece792@192.168.122.175:/home/ece792/project_codes/varfile.txt ece792@192.168.122.195:/home/ece792/project_codes/varfile.txt")
    #stdin.write('mesh@123\n')
    #print(stdout.readlines())
    ftp_client.close()
###
'''

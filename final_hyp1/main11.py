import os
import re
import json
from netmiko import ConnectHandler
from vxlan_Create import *
import paramiko
from dhcp_helper import *
import time
from TenantL3comm import *
tenant_check = 0
dhcp_push = 0

class VPC:
    def __init__(self,input_dict, subnet_nos, internet_conn,subnet_dict):
        global tenant_check, dhcp_push
        try:
            with open("./counter.txt", "r+") as w:
                each_line = w.readlines()
                for each in each_line:
                    if "tenant_count" in each:
                        count = each.split("=")[1]
                        tenant_check = int(count) + 1
        except:
            with open("./counter.txt", 'w+') as w:
                w.write("tenant_count=0\n")
        with open("./counter.txt","w+") as w:
            w.write("tenant_count=" + str(tenant_check) + "\n")


    #This function hopes to create the SG and the R namespaces to provide different
    # subnet connectivity between the same tenant
    def sg_r(self,subnet_dict):
        subnet_list = []
        for key, val in subnet_dict.items():
            subnet_list.append(val)
        internet(tenant_check,subnet_list,internet_conn)
    #This function hopes to create the l2 bridge and the network for it
    #You need to modify vars file for this

    def spin_l2_bridges(self,no_vms,each):
                    #Tenant57SG_1
        #Integrating Mesh code here for VxLAN Creation!
        '''
        NS_tenant1_1 - Vxlan Namespace
        Tenant1_SG_1 - SG Namespace
        tenant1br_1 - OVS Bridge Name
        '''
        to_pass = "NS_tenant" + str(tenant_check) + "_" + str(each)     #Vxlan namespace
        subnet_gateway_NS = "Tenant" + str(tenant_check) + "_SG_" + str(each)      #subnet_gateway namespace
        Create_NS(str(to_pass))
        #Called the function to create SG and the VxLAN gateway (TG)
        print("ovs_l2_net: tenant" + str(tenant_check) + "br")

        '''
        with open("./ansible/roles/test_role/vars/main.yml","w+") as w:
            w.write("---\n")
            w.write("# vars file for test_role\n")
            print("ovs_l2_net: tenant" + str(tenant_check) + "br" + "_" + str(each) + "\n")      #ovs_l2_net: tenant55br_1
            w.write("ovs_l2_net: tenant" + str(tenant_check) + "br" + "_" + str(each) + "\n")
            w.write("ovs_l2_br: tenant" + str(tenant_check) + "br" + "_" + str(each) +  "\n")

        with open("./ansible/roles/net_define/vars/main.yml", "w+") as w:
            w.write("---\n")
            w.write("# vars file for net_define\n")
            w.write("ovs_l2_net: tenant" + str(tenant_check) + "br" +  "_" + str(each) + "\n")
            w.write("ovs_l2_br: tenant" + str(tenant_check) + "br" + "_" + str(each) + "\n")

        print("Running the playbook for bridge creation")
        print(os.system("sudo ansible-playbook /home/ece792/vpc/ansible/bridge_main.yml"))

        '''
        print("ovs-vsctl add-br tenant"+str(tenant_check) + "br" + "_" + str(each))
        print(os.system("ovs-vsctl add-br tenant"+str(tenant_check) + "br" + "_" + str(each)))

        print("ip link set tenant"+str(tenant_check) + "br" + "_" + str(each) + " up")
        print(os.system("ip link set tenant"+str(tenant_check) + "br" + "_" + str(each) + " up"))


        #L3 veth which connects the SG to the bridge
        print("l3 veth ceation")
        print("sudo ip link add t" + str(tenant_check) + "_" + str(each) + " type veth peer name t" + str(tenant_check)+ "r")
        os.system("sudo ip link add t" + str(tenant_check) + "_" + str(each) + " type veth peer name t" + str(tenant_check)+ "r")
        os.system("sudo ip link set t" + str(tenant_check) + "_" + str(each) + " up")
        os.system("sudo ip link set t" + str(tenant_check) + "r up")

        print("sudo ovs-vsctl add-port tenant" + str(tenant_check) + "br_" + str(each) + " t" + str(tenant_check) + "_" + str(each))
        os.system("sudo ovs-vsctl add-port tenant" + str(tenant_check) + "br_" + str(each) + " t" + str(tenant_check) + "_" + str(each))

        #Adding other end of L3 veth to namespace
        '''
        print("sudo ip link set t" + str(tenant_check) + "r netns " + str(subnet_gateway_NS))
        print(os.system("sudo ip link set t" + str(tenant_check) + "r netns " + str(subnet_gateway_NS)))
        print(os.system("sudo docker exec -it " + str(subnet_gateway_NS) + " ip link set t" + str(tenant_check) + "r up"))
        '''

        pid=os.popen('docker inspect -f \'{{.State.Pid}}\' ' +str(subnet_gateway_NS)).read()
        print(pid)
        pid = pid.split('\n')[0]
        print("ip link set netns "+pid+" dev t"+str(tenant_check) + "r"  )
        os.system("ip link set netns "+pid+" dev t"+str(tenant_check) + "r" )
        print("sudo docker exec -it "+str(subnet_gateway_NS)+" ip link set t" + str(tenant_check) + "r up")
        os.system("sudo docker exec -it "+str(subnet_gateway_NS)+" ip link set t" + str(tenant_check) + "r up")


        ########## DNSMASQ GODDAMIT ############
        req_subnet = subnet_dict[str(each)]
        default_gw, dhcp_1, dhcp_2,static_config,cidr = dhcp_details(req_subnet)
        print(default_gw,dhcp_1,dhcp_2,static_config,cidr)
        #DHCP LOGIC HERE
        print("sudo docker exec -it " + str(subnet_gateway_NS) + " ip a add " + str(default_gw) + "/" + str(cidr) + " dev t" + str(tenant_check) + "r")
        print("sudo docker exec -it " + str(subnet_gateway_NS) + " dnsmasq --interface=t" + str(tenant_check) + "r --except-interface=lo --bind-interfaces --dhcp-range=" + str(dhcp_1) + "," + str(dhcp_2) + ",12h --dhcp-option=3," + str(default_gw))
        print(os.system("sudo docker exec -it " + str(subnet_gateway_NS) + " ip a add " + str(default_gw) + "/" + str(cidr) + " dev t" + str(tenant_check) + "r"))
        print(os.system("sudo docker exec -it " + str(subnet_gateway_NS) + " dnsmasq --interface=t" + str(tenant_check) + "r --except-interface=lo --bind-interfaces --dhcp-range=" + str(dhcp_1) + "," + str(dhcp_2) + ",12h --dhcp-option=3," + str(default_gw)))

        '''
        If the number of VMs exceeds 1 -> Start throwin VMs on either sides
        Needs bridge creation and TG for that on the other end.
        Note: The SG creation is only on ONE SIDE
        '''
        if int(no_vms) > 1:
            print("inga iruken ba ebba")
            to_pass = "NS_tenant" + str(tenant_check) + "_" + str(each)
            ssh_client=paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname='192.168.122.175',username='root',password='mesh@123')
            print("cd /home/ece792/vpc/ && sudo python3 ./hyp2_br1.py " + str(tenant_check) + " " + str(each))
            stdin,stdout,stderr=ssh_client.exec_command("cd /home/ece792/vpc/ && sudo python3 ./hyp2_br1.py " + str(tenant_check) + " " + str(each), get_pty=True)
            exit_status = stdout.channel.recv_exit_status()          # Blocking call
            if exit_status == 0:
                print ("Bridge_creation!")
                print(stderr)
            else:
                print("Error", exit_status)
                print(stderr)

            multicreate(str(to_pass))
            print("cd /home/ece792/vpc/ && sudo python3 ./hyp2_veth1.py " + str(tenant_check) + " " + str(each))
            stdin,stdout,stderr=ssh_client.exec_command("cd /home/ece792/vpc/ && sudo python3 ./hyp2_veth1.py " + str(tenant_check) + " " + str(each),get_pty=True)
            exit_status = stdout.channel.recv_exit_status()          # Blocking call
            if exit_status == 0:
                print ("Veth creation!")
                print(stderr)
            else:
                print("Error", exit_status)
                print(stderr)
            # domain = {'device_type': "linux",'ip': "192.168.122.175", 'username': "root", 'password': "mesh@123", 'secret': 'mesh@123'}
            # net_connect = ConnectHandler(**domain)
            # net_connect.enable()
            print("out here now")
 #           print(net_connect.send_command_timing("cd ./vpc/"))
            # print(net_connect.send_command_timing("pwd"))
            # print(net_connect.send_command_timing("cd /home/ece792/vpc/ && sudo python ./hyp2_br.py " + str(tenant_check) + " " + str(each)))
            print("TO PASSSSSSSS", to_pass)
            # print(net_connect.send_command_timing("pwd"))
            # print(net_connect.send_command_timing("sudo python ./hyp2_veth.py " + str(tenant_check) + " " + str(each)))
            print("You asked for more, give us time to bring your connections up!")
            print("Veth connection for VXLAN Creation")

            #LINK BETWEEN THE BRIDGE AND VXLAN NAMESPACE
            #Vxlan veth
            os.system("sudo ip link add t" + str(tenant_check) + "_" + str(each) + "vx type veth peer name t" + str(tenant_check) + "vxr")
            os.system("sudo ip link set t" + str(tenant_check) + "_" + str(each) + "vx up")
            #os.system("sudo ip link set t" + str(tenant_check) + "vxr up")

            #Adding one end to Ovs bridge
            os.system("sudo ovs-vsctl add-port tenant" + str(tenant_check) + "br_" + str(each) + " t" + str(tenant_check) + "_" + str(each) + "vx")
            #Adding other end of vxlan veth to namespace and then to bridge
            #os.system("sudo ip link set t" + str(tenant_check) + "vxr netns " + str(to_pass))

            pid=os.popen('docker inspect -f \'{{.State.Pid}}\' ' +str(to_pass)).read()
            print(pid)
            pid = pid.split('\n')[0]
            print("ip link set netns "+pid+" dev t"+str(tenant_check) + "vxr"  )
            os.system("ip link set netns "+pid+" dev t"+str(tenant_check) + "vxr" )




            os.system("sudo docker exec -it " + str(to_pass) + " ip link set t" + str(tenant_check) + "vxr up")
            os.system("sudo docker exec -it " + str(to_pass) + " brctl addif BR_NS t" + str(tenant_check) + "vxr")
            # net_connect.disconnect()


    '''
    This function hopes to spin the VMs the tenant reuests for:
        1. DNSMASQ needs to run on one side and on the SG of that side
        2. Tenant VMs on hyperv\isor mesh needs to get here to get their connections running
    '''
    def spin_vms(self,vm_number,sub_list,subnet_dict):
        # for each in range(1,int(no_vms) + 1):
#            Throw the VM on Hypervisor #1 if this condition suceeds
        each = vm_number
        if (int(each)%2) != 0:
            # if each == 1:
            #     subnet_gateway_NS = "Tenant" + str(tenant_check) + "_SG_" + str(c)   #CHANGE1
            #     #DHCP LOGIC HERE
            #     print("sudo docker exec -it " + str(subnet_gateway_NS) + " ip a add " + str(default_gw) + "/" + str(cidr) + " dev t" + str(tenant_check) + "r")
            #     print("sudo docker exec -it " + str(subnet_gateway_NS) + " dnsmasq --interface=t" + str(tenant_check) + "r --except-interface=lo --bind-interfaces --dhcp-range=" + str(dhcp_1) + "," + str(dhcp_2) + ",12h --dhcp-option=3," + str(default_gw))
            #     print(os.system("sudo docker exec -it " + str(subnet_gateway_NS) + " ip a add " + str(default_gw) + "/" + str(cidr) + " dev t" + str(tenant_check) + "r"))
            #     print(os.system("sudo docker exec -it " + str(subnet_gateway_NS) + " dnsmasq --interface=t" + str(tenant_check) + "r --except-interface=lo --bind-interfaces --dhcp-range=" + str(dhcp_1) + "," + str(dhcp_2) + ",12h --dhcp-option=3," + str(default_gw)))

            domain_name = "tenant" + str(tenant_check) + "vm" + str(each)    #CHANGE2
            '''
            os.system("cp ./img_to_cpy2.img /var/lib/libvirt/images/" + str(domain_name) + ".img")
            with open("./ansible/roles/gen_vm/vars/main.yml", "w+") as w:
                w.write("---\n")
                w.write("# vars file for gen_vm\n")
                w.write("domain_name: tenant" + str(tenant_check) + "vm" + str(each) + "\n")
                # w.write("network_to_attach: tenant" + str(tenant_check) + "br" + "_" + str(c) + "\n")
                w.write("vcpu: 3\n")
                w.write("image: tenant" + str(tenant_check) + "vm" + str(each) + ".img\n")

            print("Running the play for " + str(domain_name) + " creation!")
            print(os.system("sudo ansible-playbook /home/ece792/vpc/ansible/vm_create.yml"))
            time.sleep(5)
            print(os.system("sudo virsh define /etc/libvirt/qemu/" + str(domain_name) + ".xml"))
            print(os.system("sudo virsh start " + str(domain_name)))

                print("EACH",str(each_subnet))
                print("Subnet_list", str(subnet_dict))

                virsh attach-interface --domain vm1 --type network
                --source openstackvms --model virtio
                --mac 52:54:00:4b:73:5f --config --live

                print("sudo virsh attach-interface --domain " + str(domain_name) + " --type network --source tenant" + str(tenant_check) + "br_" + str(each_subnet))
                print(os.system("sudo virsh attach-interface --domain " + str(domain_name) + " --type network --source tenant" + str(tenant_check) + "br_" + str(each_subnet)))

                '''
            os.system("docker run --name "+domain_name+" --cap-add=NET_ADMIN -itd main-vm")
            print("docker run --name "+domain_name+" --cap-add=NET_ADMIN -itd main-vm")

            print("sudo docker exec -it "+domain_name+" ip route del default")
            os.system("sudo docker exec -it "+domain_name+" ip route del default")

            for each_subnet in sub_list:
                os.system("ovs-docker add-port tenant" + str(tenant_check) + "br_" + str(each_subnet) + " "+"eth"+str(each_subnet)+" "+str(domain_name))
                print("ovs-docker add-port tenant" + str(tenant_check) + "br_" + str(each_subnet) + " "+"eth"+str(each_subnet)+" "+str(domain_name))
                print("sudo docker exec -it "+domain_name+" dhclient eth"+str(each_subnet))
                os.system("sudo docker exec -it "+domain_name+" dhclient eth"+str(each_subnet))




#            Throw the VM on Hypersor #2 if this condition suceeds
        elif int(each)%2 == 0:


            domain_name = "tenant" + str(tenant_check) + "vm" + str(each)
            ssh_client=paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname='192.168.122.175',username='root',password='mesh@123')
            print("VM on creation on the other hypervisor!!")
            '''
            print("bash /home/ece792/vpc/runner.sh " + str(tenant_check) + " " + str(domain_name) + " " + str(each))
            stdin,stdout,stderr=ssh_client.exec_command("bash /home/ece792/vpc/runner.sh " + str(tenant_check) + " " + str(domain_name) + " " + str(each), get_pty=True)

            exit_status = stdout.channel.recv_exit_status()          # Blocking call
            if exit_status == 0:
                print ("Success-pt1!")
                print(stderr)
            else:
                print("Error", exit_status)
                print(stderr)
            print ("bash /home/ece792/vpc/runner_pt2.sh " + str(tenant_check) + " " + str(domain_name) + " " + str(each))
            stdin,stdout,stderr=ssh_client.exec_command("bash /home/ece792/vpc/runner_pt2.sh " + str(tenant_check) + " " + str(domain_name) + " " + str(each), get_pty=True)

            exit_status = stdout.channel.recv_exit_status()          # Blocking call
            if exit_status == 0:
                print ("Success-pt2!")
                print(stderr)
            else:
                print("Error", exit_status)
                print(stderr)

                print("EACH",str(each_subnet))
                print("Subnet_list", str(subnet_dict))

                virsh attach-interface --domain vm1 --type network
                --source openstackvms --model virtio
                --mac 52:54:00:4b:73:5f --config --live

                '''
            print("python3 /home/ece792/vpc/fin_attach.py " + str(tenant_check) + " " + str(domain_name) + " " + str(each))
            stdin,stdout,stderr=ssh_client.exec_command("python3 /home/ece792/vpc/fin_attach.py " + str(tenant_check) + " " + str(domain_name) + " " + str(each) ,get_pty=True)
            exit_status = stdout.channel.recv_exit_status()          # Blocking call
            if exit_status == 0:
                print ("Success-pt3!")
                print(stderr)
            else:
                print("Error", exit_status)
                print(stderr)



            for each_subnet in sub_list:
                print("python3 /home/ece792/vpc/final_vm_attach1.py " + str(tenant_check) + " " + str(domain_name) + " " + str(each) + " " + str(each_subnet))
                stdin,stdout,stderr=ssh_client.exec_command("python3 /home/ece792/vpc/final_vm_attach1.py " + str(tenant_check) + " " + str(domain_name) + " " + str(each) + " " + str(each_subnet),get_pty=True)
                exit_status = stdout.channel.recv_exit_status()          # Blocking call
                if exit_status == 0:
                    print ("Success-pt3!")
                    print(stderr)
                else:
                    print("Error", exit_status)
                    print(stderr)


'''
***************************************
    USER INPUTS! + Computations!
***************************************
'''


subnet_nos = 0
subnet_dict = {}
vm_nos = 0
new_dict = {}
internet_conn = ''
input_dict = {}
mgmt = ''

with open('input_reader.json','r+') as reader:
    data = json.load(reader)

    # print(data)
    subnet_nos = data["subnet_nos"]
    subnet_dict = data["subnet_dict"]
    vm_nos = data["vm_nos"]
    new_dict = data["new_dict"]
    internet_conn = data["Internet"]
    mgmt = data["Management"]

for k,v in subnet_dict.items():
    temp_val = 0
    for key,val in new_dict.items():
        if str(k) in val:
            temp_val += 1
    input_dict[str(k)] = temp_val


print("************************TENANT INFO*****************************")
print("* Number of subnets: {}".format(str(subnet_nos)))
print("* Subnets asked: {}".format(str(subnet_dict)))
print("* Number of VMs asked: {}".format(str(vm_nos)))
print("* Subnets per VM requested: {}".format(str(new_dict)))
print("* Internet: {}".format(internet_conn))
print("* Management Feature: {}".format(mgmt))
print("****************************************************************")


print(input_dict)
input()
# print(subnet_dict)
tenant = VPC(input_dict, subnet_nos, internet_conn,subnet_dict)
tenant.sg_r(subnet_dict)
c = 0
for subnet,val in input_dict.items():
    c += 1
    print(subnet,val)
    tenant.spin_l2_bridges(val,c)

for vm_number,sub_list in new_dict.items():
    tenant.spin_vms(vm_number,sub_list,subnet_dict)
    #tenant.spin_vms(val,default_gw,dhcp_1,dhcp_2,c,cidr)
print("*** Origin server Origin{} creation ***".format(str(tenant_check)))

output = os.system("sudo python3 /home/ece792/vpc/origin_server.py " + str(tenant_check))




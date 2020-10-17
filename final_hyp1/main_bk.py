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
        # self.no_vms = no_vms
        # self.default_gw = default_gw
        # self.dhcp_1 = dhcp_1
        # self.dhcp_2 = dhcp_2
        # if int(no_vms) %2 != 0:
        #     dhcp_push = 1
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
        for subnet, no_vms in input_dict.items():
            subnet_list.append(subnet)
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

        #L3 veth which connects the SG to the bridge
        print("l3 veth ceation")
        print("sudo ip link add t" + str(tenant_check) + "_" + str(each) + " type veth peer name t" + str(tenant_check) + "r")
        os.system("sudo ip link add t" + str(tenant_check) + "_" + str(each) + " type veth peer name t" + str(tenant_check) + "r")
        os.system("sudo ip link set t" + str(tenant_check) + "_" + str(each) + " up")
        print("sudo ovs-vsctl add-port tenant" + str(tenant_check) + "br_" + str(each) + " t" + str(tenant_check) + "_" + str(each))
        os.system("sudo ovs-vsctl add-port tenant" + str(tenant_check) + "br_" + str(each) + " t" + str(tenant_check) + "_" + str(each))

        #Adding other end of L3 veth to namespace
        print("sudo ip link set t" + str(tenant_check) + "r netns " + str(subnet_gateway_NS))
        print(os.system("sudo ip link set t" + str(tenant_check) + "r netns " + str(subnet_gateway_NS)))
        print(os.system("sudo ip netns exec " + str(subnet_gateway_NS) + " ip link set t" + str(tenant_check) + "r up"))

        ########## DNSMASQ GODDAMIT ############
        req_subnet = subnet_dict[int(each)]
        default_gw, dhcp_1, dhcp_2,static_config,cidr = dhcp_details(req_subnet)
        print(default_gw,dhcp_1,dhcp_2,static_config,cidr)
        #DHCP LOGIC HERE
        print("sudo ip netns exec " + str(subnet_gateway_NS) + " ip a add " + str(default_gw) + "/" + str(cidr) + " dev t" + str(tenant_check) + "r")
        print("sudo ip netns exec " + str(subnet_gateway_NS) + " dnsmasq --interface=t" + str(tenant_check) + "r --except-interface=lo --bind-interfaces --dhcp-range=" + str(dhcp_1) + "," + str(dhcp_2) + ",12h --dhcp-option=3," + str(default_gw))
        print(os.system("sudo ip netns exec " + str(subnet_gateway_NS) + " ip a add " + str(default_gw) + "/" + str(cidr) + " dev t" + str(tenant_check) + "r"))
        print(os.system("sudo ip netns exec " + str(subnet_gateway_NS) + " dnsmasq --interface=t" + str(tenant_check) + "r --except-interface=lo --bind-interfaces --dhcp-range=" + str(dhcp_1) + "," + str(dhcp_2) + ",12h --dhcp-option=3," + str(default_gw)))

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
            stdin,stdout,stderr=ssh_client.exec_command("cd /home/ece792/vpc/ && sudo python3 ./hyp2_br.py " + str(tenant_check) + " " + str(each))
            exit_status = stdout.channel.recv_exit_status()          # Blocking call
            if exit_status == 0:
                print ("Bridge_creation!")
                print(stderr)
            else:
                print("Error", exit_status)
                print(stderr)
            
            multicreate(str(to_pass))

            stdin,stdout,stderr=ssh_client.exec_command("cd /home/ece792/vpc/ && sudo python3 ./hyp2_veth.py " + str(tenant_check) + " " + str(each))
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
            #Adding one end to Ovs bridge
            os.system("sudo ovs-vsctl add-port tenant" + str(tenant_check) + "br_" + str(each) + " t" + str(tenant_check) + "_" + str(each) + "vx")
            #Adding other end of vxlan veth to namespace and then to bridge
            os.system("sudo ip link set t" + str(tenant_check) + "vxr netns " + str(to_pass))
            os.system("sudo ip netns exec " + str(to_pass) + " ip link set t" + str(tenant_check) + "vxr up")
            os.system("sudo ip netns exec " + str(to_pass) + " brctl addif BR_NS t" + str(tenant_check) + "vxr")
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
            #     print("sudo ip netns exec " + str(subnet_gateway_NS) + " ip a add " + str(default_gw) + "/" + str(cidr) + " dev t" + str(tenant_check) + "r")
            #     print("sudo ip netns exec " + str(subnet_gateway_NS) + " dnsmasq --interface=t" + str(tenant_check) + "r --except-interface=lo --bind-interfaces --dhcp-range=" + str(dhcp_1) + "," + str(dhcp_2) + ",12h --dhcp-option=3," + str(default_gw))
            #     print(os.system("sudo ip netns exec " + str(subnet_gateway_NS) + " ip a add " + str(default_gw) + "/" + str(cidr) + " dev t" + str(tenant_check) + "r"))
            #     print(os.system("sudo ip netns exec " + str(subnet_gateway_NS) + " dnsmasq --interface=t" + str(tenant_check) + "r --except-interface=lo --bind-interfaces --dhcp-range=" + str(dhcp_1) + "," + str(dhcp_2) + ",12h --dhcp-option=3," + str(default_gw)))

            domain_name = "tenant" + str(tenant_check) + "vm" + str(each)    #CHANGE2
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
            for each_subnet in sub_list:
                print("EACH",str(each_subnet))
                print("Subnet_list", str(subnet_dict))
                '''
                virsh attach-interface --domain vm1 --type network
                --source openstackvms --model virtio
                --mac 52:54:00:4b:73:5f --config --live
                '''
                print("sudo virsh attach-interface --domain " + str(domain_name) + " --type network --source tenant" + str(tenant_check) + "br_" + str(each_subnet))
                print(os.system("sudo virsh attach-interface --domain " + str(domain_name) + " --type network --source tenant" + str(tenant_check) + "br_" + str(each_subnet)))

#            Throw the VM on Hypersor #2 if this condition suceeds
        elif int(each)%2 == 0:
            domain_name = "tenant" + str(tenant_check) + "vm" + str(each)
            ssh_client=paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname='192.168.122.175',username='root',password='mesh@123')
            print("VM on creation on the other hypervisor!!")
            print("bash /home/ece792/vpc/runner.sh " + str(tenant_check) + " " + str(domain_name) + " " + str(each))
            stdin,stdout,stderr=ssh_client.exec_command("bash /home/ece792/vpc/runner.sh " + str(tenant_check) + " " + str(domain_name) + " " + str(each))

            exit_status = stdout.channel.recv_exit_status()          # Blocking call
            if exit_status == 0:
                print ("Success-pt1!")
                print(stderr)
            else:
                print("Error", exit_status)
                print(stderr)
            print ("bash /home/ece792/vpc/runner_pt2.sh " + str(tenant_check) + " " + str(domain_name) + " " + str(each))
            stdin,stdout,stderr=ssh_client.exec_command("bash /home/ece792/vpc/runner_pt2.sh " + str(tenant_check) + " " + str(domain_name) + " " + str(each))

            exit_status = stdout.channel.recv_exit_status()          # Blocking call
            if exit_status == 0:
                print ("Success-pt2!")
                print(stderr)
            else:
                print("Error", exit_status)
                print(stderr)
            for each_subnet in sub_list:
                print("EACH",str(each_subnet))
                print("Subnet_list", str(subnet_dict))
                '''
                virsh attach-interface --domain vm1 --type network
                --source openstackvms --model virtio
                --mac 52:54:00:4b:73:5f --config --live
                '''
                print("python3 /home/ece792/vpc/vm_final_attach.py " + str(tenant_check) + " " + str(domain_name) + " " + str(each) + " " + str(each_subnet))
                stdin,stdout,stderr=ssh_client.exec_command("python3 /home/ece792/vpc/final_vm_attach.py " + str(tenant_check) + " " + str(domain_name) + " " + str(each) + " " + str(each_subnet))
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

subnet_nos  = input("Enter the number of subnets required: ")
subnet_dict = {}
input_dict = {}
new_dict = {}
for each in range(1,int(subnet_nos)+1):
    ip = input("Enter the subnet for subnet #" + str(each) + ": ")
    subnet_dict[each] = ip


vm_nos = int(input("Enter the no of VMs : " ))

#input_dict[str(ip)] = str(vm_nos)
for each in range(1,vm_nos+1):
    print("Available subnets!")
    print(subnet_dict)
    per_vm_detail = input("Enter the subnets needed for this VM separated by commas (0,1,2...): ")
    temp_list = per_vm_detail.split(',')
    new_dict[each] = temp_list
internet_conn = input("Do you want internet? (Yes/No)")
print(new_dict)
for k,v in subnet_dict.items():
    temp_val = 0
    for key,val in new_dict.items():
        if str(k) in val:
            temp_val += 1
    input_dict[str(k)] = temp_val
print(input_dict)
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

#with open('./func_feature_helper.txt') as w:
#    for k,v in to_send.items():
#        w.write(str(k) + "/" + str(v))
#        w.write('\n')


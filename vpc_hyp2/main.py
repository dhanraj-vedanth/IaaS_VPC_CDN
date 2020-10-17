import os
import re
import commands
import json
# import libvirt
tenant_check = 0

class VPC:
    def __init__(self,no_vms):
        global tenant_check
        self.no_vms = no_vms
        tenant_check += 1
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

    #This function hopes to create the l2 bridge and the network for it
    #You need to modify vars file for this
    def spin_l2_bridges(self):
        print(tenant_check)
        print("ovs_l2_net: t" + str(tenant_check) + "br")
        with open("./ansible/roles/test_role/vars/main.yml","w+") as w:
            w.write("---\n")
            w.write("# vars file for test_role\n")
            w.write("ovs_l2_net: tenant" + str(tenant_check) + "br" + "\n")
            w.write("ovs_l2_br: tenant" + str(tenant_check) + "br" + "\n")

        with open("./ansible/roles/net_define/vars/main.yml", "w+") as w:
            w.write("---\n")
            w.write("# vars file for net_define\n")
            w.write("ovs_l2_net: tenant" + str(tenant_check) + "br" + "\n")
            w.write("ovs_l2_br: tenant" + str(tenant_check) + "br" + "\n")

        print("Running the playbook")
        print(commands.getoutput("sudo ansible-playbook ./ansible/bridge_main.yml"))

    def spin_vms(self):
        for each in range(1,int(self.no_vms) + 1):
            domain_name = "tenant" + str(tenant_check) + "vm" + str(each)
            commands.getoutput("cp ./img_to_cpy.img /var/lib/libvirt/images/" + str(domain_name) + ".img")
            with open("./ansible/roles/gen_vm/vars/main.yml", "w+") as w:
                # print("---\n")
                # print("domain_name: tenant" + str(tenant_check) + "vm" + str(each) + "\n")
                # print("network_to_attach: tenant" + str(tenant_check) + "vm" + str(each) + "\n")
                # print("image:/var/lib/libvirt/images/tenant" + str(tenant_check) + "vm" + str(each) + ".img\n")
                w.write("---\n")
                w.write("# vars file for gen_vm\n")
                w.write("domain_name: tenant" + str(tenant_check) + "vm" + str(each) + "\n")
                w.write("network_to_attach: tenant" + str(tenant_check) + "br" + "\n")
                w.write("vcpu: 3\n")
                w.write("image: tenant" + str(tenant_check) + "vm" + str(each) + ".img\n")

            print("Running the play for " + str(domain_name) + " creation!")
            print(commands.getoutput("sudo ansible-playbook ./ansible/vm_create.yml"))
            print(commands.getoutput("sudo virsh define /etc/libvirt/qemu/" + str(domain_name) + ".xml"))
            print(commands.getoutput("sudo virsh start " + str(domain_name)))
            
                

main_input = input("Enter the number of vms you require: ")

tenant = VPC(int(main_input))
tenant.spin_l2_bridges()
tenant.spin_vms()

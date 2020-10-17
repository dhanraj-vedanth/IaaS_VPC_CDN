import re
import json
import sys
import os

tenant_check = int(sys.argv[1])
domain_name = sys.argv[2]
each = int(sys.argv[3])
# c = int(sys.argv[4])

#opss= os.system("sudo cp ./img_to_cpy.img /var/lib/libvirt/images/" + str(domain_name) + ".img")
print(tenant_check,domain_name,each)
def spin_vms(tenant_check,domain_name,each):
    domain_name = "tenant" + str(tenant_check) + "vm" + str(each)
    #opss= os.system("sudo cp ./img_to_cpy.img /var/lib/libvirt/images/" + str(domain_name) + ".img")
    #print(opss)
    print("Image build for the VM!")
    with open("/home/ece792/vpc/ansible/roles/gen_vm/vars/main.yml", "w+") as w:
        print("---\n")
        print("domain_name: tenant" + str(tenant_check) + "vm" + str(each) +  "\n")
        print("network_to_attach: tenant" + str(tenant_check) + "vm" + str(each) + "\n")
        print("image:/var/lib/libvirt/images/tenant" + str(tenant_check) + "vm" + str(each) + ".img\n")
        w.write("---\n")
        w.write("# vars file for gen_vm\n")
        w.write("domain_name: tenant" + str(tenant_check) + "vm" + str(each) + "\n")
        # w.write("network_to_attach: tenant" + str(tenant_check) + "br" + "_" + str(c) + "\n")
        w.write("vcpu: 3\n")
        w.write("image: tenant" + str(tenant_check) + "vm" + str(each) + ".img\n")

    print("Running the play for " + str(domain_name) + " creation!")
#    opx = os.system("pwd")
#    op1 = os.system("sudo ansible-playbook /home/ece792/vpc/ansible/vm_create.yml")
#    print(op1)
#    op2 = os.system("sudo virsh define /etc/libvirt/qemu/" + str(domain_name) + ".xml")
#    print(op2)
#    op3 = os.system("sudo virsh start " + str(domain_name))
#    print(op3)

spin_vms(tenant_check,domain_name,each)


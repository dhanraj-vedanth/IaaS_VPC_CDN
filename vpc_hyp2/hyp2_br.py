import os
import re
import json
import sys
# import libvirt


#This function hopes to create the l2 bridge and the network for it
#You need to modify vars file for this
tenant_check = int(sys.argv[1])
each = int(sys.argv[2])

print(tenant_check,each)
def spin_l2_bridges(tenant_check,each):
    print(tenant_check)
    print("ovs_l2_net: t" + str(tenant_check) + "br")
    with open("./ansible/roles/test_role/vars/main.yml","w+") as w:
        w.write("---\n")
        w.write("# vars file for test_role\n")
        w.write("ovs_l2_net: tenant" + str(tenant_check) + "br" + "_" + str(each) + "\n")
        w.write("ovs_l2_br: tenant" + str(tenant_check) + "br" + "_" + str(each) + "\n")

# ovs_l2_net: tenant" + str(tenant_check) + "br" + "_" + str(each) + "\n"

    with open("./ansible/roles/net_define/vars/main.yml", "w+") as w:
        w.write("---\n")
        w.write("# vars file for net_define\n")
        w.write("ovs_l2_net: tenant" + str(tenant_check) + "br" + "_" + str(each) + "\n")
        w.write("ovs_l2_br: tenant" + str(tenant_check) + "br" + "_" + str(each) + "\n")

    print("Running the playbook")
    output = os.system("sudo ansible-playbook ./ansible/bridge_main.yml")
    print(output)

spin_l2_bridges(tenant_check,each)



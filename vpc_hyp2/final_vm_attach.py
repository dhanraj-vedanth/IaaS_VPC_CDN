import os 
import sys

tenant_check = int(sys.argv[1])
domain_name = sys.argv[2]
each = int(sys.argv[3])
subnet = sys.argv[4]
# subnet_dict = sys.argv[5]


# for each_subnet in sub_list:
print("sudo virsh attach-interface --domain " + str(domain_name) + " --type network --source tenant" + str(tenant_check) + "br_" + str(subnet))
print(os.system("sudo virsh attach-interface --domain " + str(domain_name) + " --type network --source tenant" + str(tenant_check) + "br_" + str(subnet)))


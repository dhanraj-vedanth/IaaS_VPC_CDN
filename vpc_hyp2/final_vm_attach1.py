import os
import sys

tenant_check = int(sys.argv[1])
domain_name = sys.argv[2]
each = int(sys.argv[3])
each_subnet = sys.argv[4]
# subnet_dict = sys.argv[5]

#os.system("docker run --name "+str(domain_name)+" --cap-add=NET_ADMIN -itd main-vm")
#print("docker run --name "+str(domain_name)+" --cap-add=NET_ADMIN -itd main-vm")
os.system("ovs-docker add-port tenant" + str(tenant_check) + "br_" + str(each_subnet) + " "+"eth"+str(each_subnet)+" "+str(domain_name))
print("ovs-docker add-port tenant" + str(tenant_check) + "br_" + str(each_subnet) + " "+"eth"+str(each_subnet)+" "+str(domain_name))
print("sudo docker exec -it "+domain_name+" dhclient eth"+str(each_subnet))
os.system("sudo docker exec -it "+domain_name+" dhclient eth"+str(each_subnet))

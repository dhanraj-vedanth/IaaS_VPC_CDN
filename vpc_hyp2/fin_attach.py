import os
import sys

tenant_check = int(sys.argv[1])
domain_name = sys.argv[2]
each = int(sys.argv[3])
#subnet = sys.argv[4]
# subnet_dict = sys.argv[5]

os.system("docker run --name " +str(domain_name) +" --cap-add=NET_ADMIN -itd main-vm")
print( "docker run --name " +str(domain_name) +" --cap-add=NET_ADMIN -itd main-vm")

print("sudo docker exec -it "+domain_name+" ip route del default")
os.system("sudo docker exec -it "+domain_name+" ip route del default")

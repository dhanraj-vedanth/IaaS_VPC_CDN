import sys
import os

tenant_check = int(sys.argv[1])
domain_name = sys.argv[2]
each = int(sys.argv[3])
print("Running the play for " + str(domain_name) + " creation!")
opx = os.system("pwd")
op1 = os.system("sudo ansible-playbook /home/ece792/vpc/ansible/vm_create.yml")
print(op1)

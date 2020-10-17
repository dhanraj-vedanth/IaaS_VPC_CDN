import os
import paramiko
noclient=input("Tenant number?")
novm=input("how many vms did he ask for")
novm=int(novm)
for j in range(novm):
	if j==0: 
		j=j+1;
	os.system("sudo virsh destroy tenant"+noclient+"vm"+str(j))
	os.system("sudo virsh undefine tenant"+noclient+"vm"+str(j))
os.system("brctl delif t"+noclient)
os.system("sudo ifconfig tenant"+noclient+"br down")
os.system("sudo brctl delbr tenant"+noclient)

import os
import sys
import re
import subprocess

pat = '[0-9]+\w+\s+\w+\s+\S+'

current_docker = subprocess.getoutput("sudo docker ps")

curr_list = []
old_list = []
for each in current_docker.splitlines():
    match = re.match(r'(.*\s+(\S+))', each)
    if match:
        if match.group(2) != 'NAMES':
            curr_list.append(match.group(2))


with open('/home/ece792/vpc/management/useless_checker/monitor.txt','r+') as w:
    lines = w.read().splitlines()
    for each_line in lines:
        old_list.append(each_line)

#print(curr_list)
#print("**********")
#print(old_list)



diff = list(set(old_list) - set(curr_list))
print("We died!",diff)

for cont in diff:
    print("Spawning edge node {}".format(cont))
    subprocess.getoutput("sudo docker start {}".format(cont))


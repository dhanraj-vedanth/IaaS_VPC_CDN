import os
import sys
import re
import subprocess

pat = '[0-9]+\w+\s+\w+\s+\S+'

current_docker = subprocess.getoutput("sudo docker ps")

curr_list = []
for each in current_docker.splitlines():
    match = re.match(r'(.*\s+(\S+))', each)
    if match:
        if match.group(2) != 'NAMES':
            curr_list.append(match.group(2))

#print(curr_list)

with open('/home/ece792/vpc/management/useless_checker/monitor.txt', 'w+') as w:
    for each in curr_list:
        w.write(each)
        w.write('\n')


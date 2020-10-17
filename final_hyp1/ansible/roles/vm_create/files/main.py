import subprocess
from netmiko import ConnectHandler
import time 
import re
from variables import *

time.sleep(40)
for each in dom_list:
    out = subprocess.getoutput("sudo virsh domifaddr " + str(each))
    print(out)
    pat = '(\S+\s+\S+\s+\S+\s+(\d+\.\d+\.\d+\.\d+)\/\S+)'
    matched = re.search(pat,out)
    ip = matched.group(2)
    print(ip)
    domain = {'device_type': "linux",'ip': str(ip), 'username': "draghun", 'password': "hourglass", 'secret': 'hourglass'}
    try:
        net_connect = ConnectHandler(**domain)
        net_connect.enable()
    except:
        print("Connection Failure")
    print("Starting wireshark")
    net_connect.send_command("sudo yum -y install wireshark")
    print("Done with wireshark")
    print("Starting installation of iperf")
    net_connect.send_command("yum -y install epel-release")
    net_connect.send_command("yum -y install iperf")
    print("ALL DONE!")





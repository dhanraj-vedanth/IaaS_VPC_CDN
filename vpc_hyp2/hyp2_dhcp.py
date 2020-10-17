import commands
import sys


tenant_check = sys.argv[1]
default_gw = sys.argv[2]
dhcp_1 = sys.argv[3]
dhcp_2 = sys.argv[4]


def create_dhcp(tenant_check, default_gw, dhcp_1, dhcp_2):
    os.system("sudo ip netns exec NS_tenant" + str(tenant_check) + " ip a add " + str(default_gw) + " dev t" + str(tenant_check))
    os.system("sudo ip netns exec NS_tenant" + str(tenant_check) + " dnsmasq --interface=t" + str(tenant_check) + " --except-interface=lo --bind-interfaces --dhcp-range=" + str(dhcp_1) + "," + str(dhcp_2) + ",12h --dhcp-option=3," + str(default_gw))


create_dhcp(tenant_check, default_gw, dhcp_1, dhcp_2)

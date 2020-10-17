import ipaddress



def dhcp_details(ip):
    ip_addr = ip.split('/')[0]
    cidr = ip.split('/')[1]

    print(ip_addr)
    print(cidr)
    total = ipaddress.ip_network(str(ip_addr) + '/' + str(cidr))
    print("The subnet mask is: " + str(total.netmask))
    ip_list = []
    usable_ips = total.hosts()

    for each in usable_ips:
        ip_list.append(str(each))
    print("\nDefault gateway is: ", str(ip_list[0]))
    print("DHCP range:", str(ip_list[1]), str(ip_list[-1]))

    return(str(ip_list[0]), str(ip_list[1]), str(ip_list[-1]))


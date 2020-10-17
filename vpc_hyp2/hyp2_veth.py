import sys
import os

tenant_check = sys.argv[1]
each = sys.argv[2]

def create_veths(tenant_check,each):
    #LINK BETWEEN THE BRIDGE AND VXLAN NAMESPACE
    #L3 veth
    print("VETH FUNCTION ON THEIR END??????")
    # sudo ip link set t" + str(tenant_check) + "_" + str(each) + " up"
    # sudo ip link set t" + str(tenant_check) + "_" + str(each) + "vx up
    op1 = os.system("sudo ip link add t" + str(tenant_check) + "_" + str(each) + " type veth peer name t" + str(tenant_check) + "r")
    print(op1)
    op2 = os.system("sudo ip link set t" + str(tenant_check) + "_" + str(each) + " up")
    print(op2)
    #Vxlan veth
    print(os.system("sudo ip link add t" + str(tenant_check) + "_" + str(each) + "vx type veth peer name t" + str(tenant_check) + "vxr"))
    print(os.system("sudo ip link set t" + str(tenant_check) + "_" + str(each) + "vx up"))
    #Adding one end to Ovs bridge
    # "sudo ovs-vsctl add-port tenant" + str(tenant_check) + "br_" + str(each) + " t" + str(tenant_check) + "_" + str(each)
    # "sudo ovs-vsctl add-port tenant" + str(tenant_check) + "br_" + str(each) + " t" + str(tenant_check) + "_" + str(each) + "vx"
    print(os.system("sudo ovs-vsctl add-port tenant" + str(tenant_check) + "br_" + str(each) + " t" + str(tenant_check) + "_" + str(each)))
    print(os.system("sudo ovs-vsctl add-port tenant" + str(tenant_check) + "br_" + str(each) + " t" + str(tenant_check) + "_" + str(each) + "vx"))
    #Adding other end of L3 veth to namespace
    print(os.system("sudo ip link set t" + str(tenant_check) + "r netns NS_tenant" + str(tenant_check) + "_" + str(each)))
    print(os.system("sudo ip netns exec NS_tenant" + str(tenant_check) + "_" + str(each) + " ip link set t" + str(tenant_check) + "r up"))
    #Adding other end of vxlan veth to namespace and then to bridge
    print(os.system("sudo ip link set t" + str(tenant_check) + "vxr netns NS_tenant" + str(tenant_check) + "_" + str(each)))
    print(os.system("sudo ip netns exec NS_tenant" + str(tenant_check) + "_" + str(each) + " ip link set t" + str(tenant_check) + "vxr up"))
    print(os.system("sudo ip netns exec NS_tenant" + str(tenant_check) + "_" + str(each) + " brctl addif BR_NS t" + str(tenant_check) + "vxr"))
    print("out of the stupid veth")


create_veths(tenant_check,each)

import re

'''
---

- name: Creating two VMs with user's requirements (Define in vars) - creating 1stVM
  command: "sudo virt-install -n {{ item.dom_name }} -r {{ item.ram }} --vcpu={{ item.vcpu }} --cpu host --disk path=/var/lib/libvirt/images/{{ item.dom_name }}.img,size={{ item.disk }} --network network=default --network network={{ item.net1 }} --network network={{ item.net2 }} -c {{ item.ios_path }} -v"
  with_items:
     - { dom_name: "{{ dom_name1 }}", vcpu: "{{ vcpus }}", ram: "{{ ram }}", disk: "{{ disk }}", ios_path: "{{ ios_path }}", net1: "{{ internet }}", net2: "{{ ovs_l2_net }}" }
'''


def vm_create1(int1,k):
    with open("./playbook" + str(k) + ".yml","w+") as w:
        w.write("---\n")
        w.write("- name: Creating VM with user Req.\n")
        w.write("  hosts: 127.0.0.1\n")
        w.write("  tasks:\n")
        w.write("  - name: Creating VM with one interface according to user's requirements\n")
        w.write("    command: sudo virt-install -n autovm" + str(k) + " -r 1024 --vcpu=3 --cpu host --disk path=/var/lib/libvirt/images/autovm" + str(k) + ".img,size=10 --network network=default --network network=" + str(int1) + " -c /home/CentOS-7-x86_64-Minimal-1609-99.iso --noautoconsole")



def vm_create2(int1,int2,k):
    with open("./playbook" + str(k) + ".yml","w+") as w:
        w.write("---\n")
        w.write("- name: Creating VM with user Req.\n")
        w.write("  hosts: 127.0.0.1\n")
        w.write("  tasks:\n")
        w.write("  - name: Creating VM with two interfaces according to user's requirements\n")
        w.write("    command: sudo virt-install -n autovm" + str(k) + " -r 1024 --vcpu=3 --cpu host --disk path=/var/lib/libvirt/images/autovm" + str(k) + ".img,size=10 --network network=default --network network=" + str(int1) + " --network network=" + str(int2) + " -c /home/CentOS-7-x86_64-Minimal-1609-99.iso --noautoconsole")

def vm_create3(int1,int2,int3,k):
    with open("./playbook" + str(k) + ".yml","w+") as w:
        w.write("---\n")
        w.write("- name: Creating VM with user Req.\n")
        w.write("  hosts: 127.0.0.1\n")
        w.write("  tasks:\n")
        w.write("  - name: Creating VM with three interfaces according to user's requirements\n")
        w.write("    command: sudo virt-install -n autovm" + str(k) + " -r 1024 --vcpu=3 --cpu host --disk path=/var/lib/libvirt/images/autovm" + str(k) + ".img,size=10 --network network=default --network network=" + str(int1) + " --network network=" + str(int2) + " --network network=" + str(int3) +  " -c /home/CentOS-7-x86_64-Minimal-1609-99.iso --noautoconsole")



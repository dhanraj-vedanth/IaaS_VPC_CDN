#!/bin/bash

tenant_check=${1}
domain_name=${2}
each=${3}

echo ${domain_name}
sudo ansible-playbook /home/ece792/vpc/ansible/vm_create.yml
echo ${op1}
op2="$(sudo virsh define /etc/libvirt/qemu/${domain_name}.xml)"
echo ${op2}
op3="$(sudo virsh start ${domain_name})"
echo ${op3}


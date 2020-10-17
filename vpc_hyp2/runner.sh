#!/bin/bash

tenant_check=${1}
domain_name=${2}
each=${3}

main_op="$(sudo python /home/ece792/vpc/vm_create.py ${tenant_check} ${domain_name} ${each})"
echo "${main_op}"
sudo cp /home/ece792/vpc/img_to_cpy2.img /var/lib/libvirt/images/${domain_name}.img
#main_op="$(sudo python ./vm_test.py ${tenant_check} ${domain_name} ${each})"
echo "${tenant_check}"

#op1="$(sudo ansible-playbook /home/ece792/vpc_h1/ansible/vm_create.yml)"
#echo ${op1}
#op2="$(sudo virsh define /etc/libvirt/qemu/${domain_name}.xml)"
#echo ${op2}
#op3="$(sudo virsh start ${domain_name})"
#echo ${op3}


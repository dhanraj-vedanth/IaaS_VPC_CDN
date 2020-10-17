docker exec -it $1 ip route del default 
docker exec -it $1 ip link add $4 type vxlan id $2 dev $3 dstport 4789
docker exec -it $1 bridge fdb append to 00:00:00:00:00:00 dst $5 dev $4
docker exec -it $1 ip link set $4 up
docker exec -it $1 ip route add default via $6
docker exec -it $1 brctl addif $7 $4

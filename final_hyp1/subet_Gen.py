from netaddr import *
import pprint
import math
import paramiko

def no_of_hosts(inp_2,a1,b1,ipspace):
    bl=math.ceil(math.log(inp_2+2,2))

    #print(bl)

    hs=int(math.pow(2,bl))
    #print(hs)

    a=[]
    i=1
    a.append(0)
    while True:
        f=int(hs*i)
        if (f<=65536):
            a.append(f)
            i=i+1
        else:
            break

    #print(a)
    hs1=32-bl
    ipspace=subnet_alloc(a,a1,b1,hs1,ipspace)
    return ipspace

def subnet_alloc(a,a1,b1,hs1,ipspace):
    for i in range(0,len(a)-1):
        #print(i)
        subnet=list(range(a[i],a[i+1]-1))
        result =  all(elem in ipspace  for elem in subnet)
        #print(result)
        if result:
            subnetid= a[i]
            sh=subnetid+1
            #print(ds_id)
            broadcastid= a[i+1] -1
            lh=broadcastid-1
            ds1=format(subnetid, '016b')
            #print(type(ds1))
            so_subid3= 128*int(ds1[0]) + 64*int(ds1[1]) + 32*int(ds1[2]) + 16*int(ds1[3])+ 8*int(ds1[4]) + 4*int(ds1[5]) + 2*int(ds1[6]) + int(ds1[7])
            uo_subid4= 128*int(ds1[8]) + 64*int(ds1[9]) + 32*int(ds1[10]) + 16*int(ds1[11]) + 8*int(ds1[12])+ 4*int(ds1[13]) + 2*int(ds1[14]) + int(ds1[15])
            #print(so_subid3)
            #print(uo_subid4)
            subnet_id="Subnet ID -> " +a1+'.'+b1+'.'+str(so_subid3)+'.'+str(uo_subid4)+"/"+ str(hs1)
            print(subnet_id)

            #so_subid_b=int(so_subid)


            ds1=format(broadcastid, '016b')
            so_bid3= 128*int(ds1[0]) + 64*int(ds1[1]) + 32*int(ds1[2]) + 16*int(ds1[3])+ 8*int(ds1[4]) + 4*int(ds1[5]) + 2*int(ds1[6]) + int(ds1[7])
            uo_bid4= 128*int(ds1[8]) + 64*int(ds1[9]) + 32*int(ds1[10]) + 16*int(ds1[11]) + 8*int(ds1[12])+ 4*int(ds1[13]) + 2*int(ds1[14]) + int(ds1[15])
            broadcast_id="Broadcast ID -> " +a1+'.'+b1+'.'+str(so_bid3)+'.'+str(uo_bid4)
            print(broadcast_id)

            ds1=format(sh, '016b')
            #print(type(ds1))
            so_subid3= 128*int(ds1[0]) + 64*int(ds1[1]) + 32*int(ds1[2]) + 16*int(ds1[3])+ 8*int(ds1[4]) + 4*int(ds1[5]) + 2*int(ds1[6]) + int(ds1[7])
            uo_subid4= 128*int(ds1[8]) + 64*int(ds1[9]) + 32*int(ds1[10]) + 16*int(ds1[11]) + 8*int(ds1[12])+ 4*int(ds1[13]) + 2*int(ds1[14]) + int(ds1[15])
            #print(so_subid3)
            #print(uo_subid4)
            subnet_id=a1+'.'+b1+'.'+str(so_subid3)+'.'+str(uo_subid4)
            print(subnet_id)
            g=[]
            first_usable=subnet_id
            g.append(first_usable)


            ds1=format(lh, '016b')
            so_bid3= 128*int(ds1[0]) + 64*int(ds1[1]) + 32*int(ds1[2]) + 16*int(ds1[3])+ 8*int(ds1[4]) + 4*int(ds1[5]) + 2*int(ds1[6]) + int(ds1[7])
            uo_bid4= 128*int(ds1[8]) + 64*int(ds1[9]) + 32*int(ds1[10]) + 16*int(ds1[11]) + 8*int(ds1[12])+ 4*int(ds1[13]) + 2*int(ds1[14]) + int(ds1[15])
            broadcast_id=a1+'.'+b1+'.'+str(so_bid3)+'.'+str(uo_bid4)
            print(broadcast_id)

            last_usable=broadcast_id
            g.append(last_usable)

            #print(so_bid3)
            #print(uo_bid4)
            #print(uo_bid)

            #print(b_id)
            #print('yes')
            #print(subnetid)
            #print(broadcastid)
            for i in range(subnetid,broadcastid+1):
                ipspace.remove(i)
            f=open("/home/ece792/project_codes/open1.txt","w+")
            for ele in ipspace:
                m=str(ele)
                f.write(m)
                f.write("\n")

            f.close()

            #print(ipspace[0])
            return g
        if (i==len(a)-2):
            print("Hosts cannot be allocated due to insufficient space. Try a smaller number of hosts")
            return ipspace




#inp_1=IPAddress(input('Enter class B network address\n'))
def start():
    inp_1="185.0.0.0"

    #ipspace= list(range(0, 65536))
    f=open("/home/ece792/project_codes/open1.txt","r")

    ipspace=[]
    for a1 in f:
        #a.split('\n')
        f=a1.split('\n')
        #print(f[0])
        ipspace.append(int(f[0]))

    #print(ipspace)

    a=str(inp_1).split('.')



    if(int(a[0])>=127 and int(a[0])<=191):
        print("Network ID is " + a[0]+"."+a[1]+"."+"0.0" + "/16")
        i=1
        g=[]

        while i:

            if(len(ipspace)==0):
                    print("Address space exhausted")
                    exit()
            #inp_2=int(input('Enter number of hosts required(Range-1-65534)\n'))
            inp_2=2
            print("\n")
            #a11=[]
            if (inp_2<=65534):

                a11=no_of_hosts(inp_2,a[0],a[1],ipspace)
                g.append(a11)
                i-=1
                #print(ipspace[0])
            else:
                print("Hosts cannot be accomodated.")

            print("\n")

            #inp=input('Do you want to continue (Y/N)?')

            #if(inp=='n' or inp=='N'):
                #break
    else:

        print("Not a class B address")
    print(g)
    return g

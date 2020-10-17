import json
import os
f1 = open("Client_file",'r')
f2 = json.loads(f1.read())
print(type(f2))

rfc_id = f2["RFC number"]

if f2["Type of Message (Publish/Subscribe)"]=='Publish':
    os.system("python3 dns_pub_host.py")
    print("python3 dns_pub_host.py rfc_"+rfc_id)


elif f2["Type of Message (Publish/Subscribe)"]=='Subscribe':
    if f2["Algorithm 1-Closest Server (True/False)"]=='True':
        #os.system("python3 subscribe.py")
        print("python3 subscribe.py "+rfc_id)
    elif f2["Algorithm 2-Fixed Server (True/False)"]=='True':
        Server_IP=f2["Fixed Server IP"]
        #os.system("python3 subscribe.py "+str(Server_IP))
        print("python3 subscribe_fs.py "+rfc_id+ " " +str(Server_IP))
    elif f2["Algorithm 3-Least busy server (True/False)"]=='True':
        #os.system("python3 subscribe.py")
        print("python3 subscribe_lb.py "+rfc_id)

f=open("open1.txt","w+")

ipspace= list(range(0, 65536))


for ele in ipspace:
    m=str(ele)
    f.write(m)
    f.write("\n")

f.close()

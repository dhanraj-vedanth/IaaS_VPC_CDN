f=open("open.txt","w+")

ipspace= list(range(0,32767))


for ele in ipspace:
    m=str(ele)
    f.write(m)
    f.write("\n")

f.close()




#print(m)

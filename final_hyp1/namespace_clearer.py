f = open("varfile.txt", "w+")


for i in range(1,65536):
    f.write(str(i)+"\n")


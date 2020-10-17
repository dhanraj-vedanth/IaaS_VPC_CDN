import sys
import os


for i in range(0,2):
  print(os.system("sudo ip netns del Router" + str(i)))

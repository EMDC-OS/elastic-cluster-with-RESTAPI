import os
import sys

f_read = open("/workspace/nvidia-examples/cnn/nvutils/run/pid.txt", "r")

while True:
    pid = f_read.readline()

    if not pid:
        break
    else:
        temp = "kill " + str(pid[:-1])
        os.system(temp)

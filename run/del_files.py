import os
import sys

temp = "rm /workspace/nvidia-examples/cnn/nvutils/run/pid.txt"
os.system(temp)

for i in range(4):
    temp = "rm /workspace/nvidia-examples/cnn/nvutils/run/log" + str(i) + ".txt"
    os.system(temp)

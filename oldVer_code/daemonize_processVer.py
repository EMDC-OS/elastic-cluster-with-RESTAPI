import os
import sys
import time

def start_daemon(log_file_string, gpu_index):
        try:
          pid = os.fork()

          if pid > 0:
            print('PID: %d' % pid)
            return 0

        except OSError as error:
          print('Unable to fork. Error: %d (%s)' % (error.errno, error.strerror))
          exit(0)

        doTask(log_file_string, gpu_index)

def doTask(log_file_string, gpu_index):
        os.setsid()
        os.open("/dev/null", os.O_RDWR)
        os.dup(0)
        #os.dup(0)

        with open("/workspace/nvidia-examples/cnn/nvutils/run/pid.txt", "a") as pid_file:
            pid_file.write(str(gpu_index) + ":" + str(os.getpid()) + "\n")

        check = 0

        #daemon main function
        while True:
            if check == 0:
                f_read = open(log_file_string, "a")
                f_read.write("Start\n")
                f_read.close()
                check = 1

            f_read = open(log_file_string, "a")
            #log control
            f_read.write("####KEEP LEARNING####\n")
            f_read.close()
            time.sleep(1)

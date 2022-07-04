import os
import sys
import time
import threading

def start_daemon(log_file_string, gpu_index):
        daemon_thread = threading.Thread(target = doTask, args = (log_file_string, gpu_index))
        daemon_thread.daemon = True
        daemon_thread.start()

def doTask(log_file_string, gpu_index):
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

import os
import sys
import time
import threading
import requests
import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
local_ip = s.getsockname()[0]
gpustat_time = 1

def start_daemon(log_str, gpu_index):
    daemon_thread = threading.Thread(target = doTask, args = (log_str, gpu_index))
    daemon_thread.daemon = True
    daemon_thread.start()

def doTask(log_str, gpu_index):
    global gpustat_time
    log_file_string = "/workspace/nvidia-examples/cnn/nvutils/run/" + str(local_ip) + "_log" + str(gpu_index) + ".txt"
    gpustat_open_string = "/workspace/nvidia-examples/cnn/nvutils/run/" + str(local_ip) + "_gpustat.json"
    gpustat_file_string = "gpustat --json > " + gpustat_open_string

    f = open(log_file_string, "w")
    f.write(log_str + "\n")
    f.close()
    log_string = "Start"

    while True:
        '''f_log = open(log_file_string, "r")
        log_temp = f_log.read()

        if log_string != log_temp[:-1]:
            log_string = log_temp[:-1]
            log_time = 0'''

        if gpu_index == 0:
            os.system(gpustat_file_string)
            with open(gpustat_open_string, "r") as f_gpu:
                gpu_json_data = json.load(f_gpu)

            gpu_json_data['time_now'] = gpustat_time

            with open(gpustat_open_string, "w") as f_gpu_:
                json.dump(gpu_json_data, f_gpu_, indent="\t")                                                                                                                                                                                          

            files = {'file': open(gpustat_open_string, 'rb')}
            gpustat_time += 1

            if str(local_ip) == "115.145.178.217":
                r = requests.post('http://115.145.178.218:8080/gpustat-data-tb1', files=files)
            elif str(local_ip) == "115.145.178.218":
                r = requests.post('http://115.145.178.218:8080/gpustat-data-tb2', files=files)

        #f_log.close()
        time.sleep(1)

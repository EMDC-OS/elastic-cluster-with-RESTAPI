import os
import sys
import time
import subprocess
import threading
import requests
import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
local_ip = str(s.getsockname()[0])
gpustat_time = 1

def start_daemon(log_str, hvd_local_rank):
    daemon_thread = threading.Thread(target = gpustat_control_daemon, args = (log_str, hvd_local_rank))
    daemon_thread.daemon = True
    daemon_thread.start()

def gpustat_control_daemon(log_str, hvd_local_rank):
    global gpustat_time
    gpustat_open_string = "/DTC_MaS/Job_controller_pkg/" + local_ip + "_gpustat.json"
    gpustat_file_string = "gpustat --json > " + gpustat_open_string

    while True:
        if hvd_local_rank == 0:
            os.system(gpustat_file_string)

            with open(gpustat_open_string, "r") as f_gpu:
                gpu_json_data = json.load(f_gpu)

            gpu_json_data['time_now'] = gpustat_time

            with open(gpustat_open_string, "w") as f_gpu_:
                json.dump(gpu_json_data, f_gpu_, indent="\t")

            files = {'file': open(gpustat_open_string, 'rb')}
            gpustat_time += 1

            if local_ip == "115.145.178.217":
                r = requests.post('http://115.145.178.218:8080/gpustat-data-tb1', files=files)
            elif local_ip == "115.145.178.218":
                r = requests.post('http://115.145.178.218:8080/gpustat-data-tb2', files=files)

        time.sleep(1)

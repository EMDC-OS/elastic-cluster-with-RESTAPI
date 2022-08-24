import socket
import requests
import json
from collections import OrderedDict

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ipadd = s.getsockname()[0]
node_ip = str(ipadd)

log_data = OrderedDict()

def local_log_save(global_steps, examples_per_second, elapsed_time, timestamp, local_rank):
    open_string = "/workspace/nvidia-examples/cnn/nvutils/run/" + node_ip + "_log" + str(local_rank) + ".txt"
    f_write = open(open_string, "a")

    if local_rank == 0:
        global_step_str = "global_step: " + global_steps + " images_per_sec: " + examples_per_second + "\n"
        f_write.write(global_step_str)

    elap_str = "[" + global_steps + "] " + "node/worker: "  + node_ip + "/" + str(local_rank) + " -> elapsed time: " + elapsed_time + "\n"
    cur_str = "[" + global_steps + "] " + "node/worker: "  + node_ip + "/" + str(local_rank) + " -> current time: " + timestamp + "\n"
    f_write.write(elap_str)
    f_write.write(cur_str)

    f_write.close()

def web_post(global_steps, elapsed_time, examples_per_second, local_rank):
    log_data["node"] = node_ip
    log_data["worker"] = local_rank
    log_data["global_step"] = global_steps
    log_data["elapsed_time"] = elapsed_time
    
    if local_rank == 0:
        log_data["images_per_sec"] = examples_per_second

    log_data_json = json.dumps(log_data, ensure_ascii=False, indent="\t")

    if node_ip == "115.145.178.217":
        r = requests.post('http://115.145.178.218:8080/log-data-tb1', json=log_data_json)
    elif node_ip == "115.145.178.218":
        r = requests.post('http://115.145.178.218:8080/log-data-tb2', json=log_data_json)

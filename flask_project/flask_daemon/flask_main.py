from flask import Flask, render_template, request, jsonify, make_response
from random import random
import requests
import json

app = Flask(__name__)
log_list = []
global_gpu_list = []
gpustat_list = []

is_gpu = [0, 0]
log_data_tb1_list = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
log_data_tb2_list = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]

time_now = 0
gpu_location_tb1 = ""
gpu_location_tb2 = ""

@app.route('/', methods = ['POST', 'GET'])
def update_log():
    f_read = open("/workspace/nvidia-examples/cnn/nvutils/discover_hosts.sh", "r")
    running_gpu = f_read.read()
    running_gpu_list = running_gpu.split("\n")
    del running_gpu_list[-1]

    for i in range(len(running_gpu_list)):
        temp = running_gpu_list[i].split()
        running_gpu_list[i] = temp[1]
    f_read.close()

    if request.method == 'POST':
        val = request.form
        val_list = list(val)

        gpu_list = list(request.form.listvalues())
        gpu_list_parse = gpu_list[0]
        gpu_string = gpu_list_parse[0]

        split_list = gpu_string.split(":")
        ip_address = split_list[0]
        host_num = split_list[1]

        f_write = open("/workspace/nvidia-examples/cnn/nvutils/discover_hosts.sh", "w+")
        write_string = ""
        check = 0

        for i in range(len(running_gpu_list)):
            temp = running_gpu_list[i].split(":")
            if temp[0] == ip_address:
                if val_list[0] == '+':
                    temp_num = int(temp[1]) + int(host_num)
                    temp_string = temp[0] + ":" + str(temp_num)
                    running_gpu_list[i] = temp_string
                else:
                    temp_num = int(temp[1]) - int(host_num)
                    if temp_num < 0:
                        temp_num = 0

                    temp_string = temp[0] + ":" + str(temp_num)
                    running_gpu_list[i] = temp_string

                check = 1
                break

        if check == 0 and val_list[0] == '+':
            running_gpu_list.append(gpu_string)

        for i in range(len(running_gpu_list)):
            temp = running_gpu_list[i].split(":")
            if temp[1] != '0':
                write_string = write_string + "echo " + running_gpu_list[i] + "\n"

        f_write.write(write_string)
        f_write.close()

    return render_template("main.html")

@app.route('/log_tb1', methods = ['GET', 'POST'])
def logging_tb1():
    return render_template("log_index_tb1.html")

@app.route('/log_tb2', methods = ['GET', 'POST'])
def logging_tb2():
    return render_template("log_index_tb2.html")

@app.route('/log-data-tb1', methods = ['GET', 'POST'])
def log_now_tb1():
    global log_data_tb1_list

    if request.method == 'POST':
        f_log = request.get_json(silent=True)
        log = json.loads(f_log)

        temp = []
        temp.append(log["global_step"])
        temp.append(log["elapsed_time"])
        log_data_tb1_list[log["worker"]] = temp

        if log["worker"] == 0:
            temp_i = []
            temp_i.append(log["global_step"])
            temp_i.append(log["images_per_sec"])
            log_data_tb1_list[-1] = temp_i

        response = make_response(json.dumps(log_data_tb1_list))
        response.content_type = 'application/json'
        return response                                                                                                                                                                                                                                
    else:
        response = make_response(json.dumps(log_data_tb1_list))
        response.content_type = 'application/json'
        return response

@app.route('/log-data-tb2', methods = ['GET', 'POST'])
def log_now_tb2():
    global log_data_tb2_list

    if request.method == 'POST':
        f_log = request.get_json(silent=True)
        log = json.loads(f_log)

        temp = []
        temp.append(log["global_step"])
        temp.append(log["elapsed_time"])
        log_data_tb2_list[log["worker"]] = temp

        if log["worker"] == 0:
            temp_i = []
            temp_i.append(log["global_step"])
            temp_i.append(log["images_per_sec"])
            log_data_tb2_list[-1] = temp_i

        response = make_response(json.dumps(log_data_tb2_list))
        response.content_type = 'application/json'
        return response
    else:
        response = make_response(json.dumps(log_data_tb2_list))
        response.content_type = 'application/json'
        return response

@app.route('/gpustat_tb1', methods = ['GET', 'POST'])
def gpu_stat_tb1():
    return render_template('gpu_index_tb1.html')

@app.route('/gpustat_tb2', methods = ['GET', 'POST'])
def gpu_stat_tb2():
    return render_template('gpu_index_tb2.html')

@app.route('/gpustat-data-tb1', methods = ['GET', 'POST'])
def gpustat_now_tb1():
    global is_gpu
    global gpu_location_tb1
    data = []
    default_data = [[[0, 0], [0, 1], [0, 2]], [[0, 0], [0, 1], [0, 2]], [[0, 0], [0, 1], [0, 2]], [[0, 0], [0, 1], [0, 2]]]

    if request.method == 'POST':
        f_gpustat = request.files.get('file', None)
        if f_gpustat:
            gpu_location_tb1 = '/workspace/nvidia-examples/cnn/nvutils/run/gpustat_control/' + f_gpustat.filename
            f_gpustat.save(gpu_location_tb1)
            is_gpu[0] = 1

    if is_gpu[0] == 1:
        f = open(gpu_location_tb1, "r")
        gpustat_read = f.read()
        gpustat_string = json.loads(gpustat_read)

        for i in range(4):
            temp = []

            temp1 = []
            temp1.append(gpustat_string["time_now"])
            temp1.append(gpustat_string["gpus"][i]["utilization.gpu"])
            temp.append(temp1)

            temp2 = []
            temp2.append(gpustat_string["time_now"])
            temp2.append(gpustat_string["gpus"][i]["power.draw"])
            temp.append(temp2)

            temp3 = []
            temp3.append(gpustat_string["time_now"])
            temp3.append(gpustat_string["gpus"][i]["memory.used"])
            temp.append(temp3)

            data.append(temp)

        f.close()

        response = make_response(json.dumps(data))
        response.content_type = 'application/json'
        return response

    else:
        response = make_response(json.dumps(default_data))
        response.content_type = 'application/json'
        return response

@app.route('/gpustat-data-tb2', methods = ['GET', 'POST'])
def gpustat_now_tb2():
    global is_gpu
    global gpu_location_tb2
    data = []
    default_data = [[[0, 0], [0, 1], [0, 2]], [[0, 0], [0, 1], [0, 2]], [[0, 0], [0, 1], [0, 2]], [[0, 0], [0, 1], [0, 2]]]

    if request.method == 'POST':
        f_gpustat = request.files.get('file', None)
        if f_gpustat:
            gpu_location_tb2 = '/workspace/nvidia-examples/cnn/nvutils/run/gpustat_control/' + f_gpustat.filename
            f_gpustat.save(gpu_location_tb2)
            is_gpu[1] = 1

    if is_gpu[1] == 1:
        #file open and parsing
        f = open(gpu_location_tb2, "r")
        gpustat_read = f.read()
        gpustat_string = json.loads(gpustat_read)

        for i in range(4):
            temp = []

            temp1 = []
            temp1.append(gpustat_string["time_now"])
            temp1.append(gpustat_string["gpus"][i]["utilization.gpu"])
            temp.append(temp1)

            temp2 = []
            temp2.append(gpustat_string["time_now"])
            temp2.append(gpustat_string["gpus"][i]["power.draw"])
            temp.append(temp2)

            temp3 = []
            temp3.append(gpustat_string["time_now"])
            temp3.append(gpustat_string["gpus"][i]["memory.used"])
            temp.append(temp3)

            data.append(temp)

        f.close()

        response = make_response(json.dumps(data))
        response.content_type = 'application/json'
        return response

    else:
        response = make_response(json.dumps(default_data))
        response.content_type = 'application/json'
        return response

@app.route("/update", methods=['POST'])
def update():
    gpu_string = ""
    log_list_string = ""
    global global_gpu_list
    global log_list

    f_read = open("/workspace/nvidia-examples/cnn/nvutils/discover_hosts.sh", "r")
    running_gpu = f_read.read()
    running_gpu_list = running_gpu.split("\n")
    del running_gpu_list[-1]

    for i in range(len(running_gpu_list)):
        temp = running_gpu_list[i].split()
        running_gpu_list[i] = temp[1]
        gpu_string = gpu_string + running_gpu_list[i] + "\n"

    #log_update_function
    for i in range(len(running_gpu_list)):
        check = 0
        temp1 = running_gpu_list[i].split(":")

        for k in range(len(global_gpu_list)):
            temp2 = global_gpu_list[k].split(":")
            if temp1[0] == temp2[0]:
                check = 1
                if int(temp1[1]) > int(temp2[1]):
                    log_string = '(+) ' + temp1[0] + ":" + str(int(temp1[1]) - int(temp2[1]))
                    log_list.append(log_string)
                elif int(temp1[1]) < int(temp2[1]):
                    log_string = '(-) ' + temp1[0] + ":" + str(int(temp2[1]) - int(temp1[1]))
                    log_list.append(log_string)
                break

        if check == 0:
            log_string = '(+) ' + running_gpu_list[i]
            log_list.append(log_string)

    for i in range(len(global_gpu_list)):
        check = 0
        temp1 = global_gpu_list[i].split(":")

        for k in range(len(running_gpu_list)):
            temp2 = running_gpu_list[k].split(":")
            if temp1[0] == temp2[0]:
                check = 1
                break

        if check == 0:
            log_string = '(-) ' + global_gpu_list[i]
            log_list.append(log_string)

    for i in range(len(log_list)):
        log_list_string = log_list_string + log_list[i] + "\n"

    global_gpu_list = []

    for i in range(len(running_gpu_list)):
        global_gpu_list.append(running_gpu_list[i])

    return jsonify({
        'current_gpu_list': gpu_string,
        'gpu_log': log_list_string,
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

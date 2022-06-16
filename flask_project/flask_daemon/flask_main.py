from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
log_list = []
global_gpu_list = []

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

@app.route('/log', methods = ['POST', 'GET'])
def logging():
    return render_template("logging.html")

@app.route("/log_func", methods=['POST'])
def logging_func():
    worker_log_string = ""
    worker_global_temp = ""
    worker_local_temp = ""

    f_read_worker = open("/workspace/nvidia-examples/cnn/nvutils/log.txt", "r")
    worker_load = f_read_worker.read()
    worker_load_list = worker_load.split("\n")
    del worker_load_list[-1]

    for i in range(len(worker_load_list)):
        if worker_load_list[i][0] == 'g':
            worker_global_temp = worker_global_temp + worker_load_list[i] + "\n"
        else:
            worker_local_temp = worker_local_temp + worker_load_list[i] + "\n"

    worker_log_string = worker_global_temp + "\n" + worker_local_temp

    return jsonify({
        'worker_log_string': worker_log_string,
    })

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

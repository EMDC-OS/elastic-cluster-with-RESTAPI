#!/usr/bin/env python
# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import nvutils
from resnet_model import resnet50

import os
import sys
import time
import horovod.tensorflow.keras as hvd

def start_daemon():
        try:
          pid = os.fork()

          if pid > 0:
            print('PID: %d' % pid)
            return 0

        except OSError as error:
          print('Unable to fork. Error: %d (%s)' % (error.errno, error.strerror))
          exit(0)

        doTask()

def doTask():
        os.setsid()

        os.open("/dev/null", os.O_RDWR)
        os.dup(0)
        os.dup(0)

        file_string = "/workspace/nvidia-examples/cnn/nvutils/run/log" + "0" + ".txt"

        while True:
            f_read = open(file_string, "a")
            f_read.write(str(hvd.rank()))
            f_read.close()
            time.sleep(1)

nvutils.init()

start_daemon()

default_args = {
    'image_width' : 224,
    'image_height' : 224,
    'distort_color' : False,
    'momentum' : 0.9,
    'loss_scale' : 128.0,
    # The following params can be changed by cmdline options.
    'image_format' : 'channels_last',
    'data_dir' : None,
    'data_idx_dir' : None,
    'batch_size' : 256,
    'num_iter' : 300,
    'iter_unit' : 'batch',
    'log_dir' : None,
    'export_dir' : None,
    'tensorboard_dir' : None,
    'display_every' : 10,
    'precision' : 'fp16',
    'dali_mode' : None,
    'use_xla': False,
    'predict' : False,
}

args = nvutils.parse_cmdline(default_args)

if args['predict']:
  nvutils.predict(args)
else:
  nvutils.train(resnet50, args)

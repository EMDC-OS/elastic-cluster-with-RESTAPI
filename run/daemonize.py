import os                                                                                                 
import sys
import time
import logging
import signal

import argparse

class CollectLog:
    def __init__(self, log_file=None):
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        self.logger = logging.getLogger("CollectLog")
        self.log_file = log_file
        self.__stop = False

    def main(self):
        self.logger.info("Start, PID {0}".format(os.getpid()))

        file_string = "/workspace/nvidia-examples/cnn/nvutils/run/log" + "0" + ".txt"

        while not self.__stop:
            f_read = open(file_string, "a")
            f_read.write("test\n")
            f_read.close()
            time.sleep(1)

        return 0

    def stop(self, signum, frame):
        self.__stop = True
        self.logger.info("Receive Signal {0}".format(signum))
        self.logger.info("Stop")

def run():
    collect_log = CollectLog()
    exit_code = collect_log.main()
    exit(exit_code)

def daemonize():
    # double fork, first fork
    pid = os.fork()
    if pid > 0:
        exit(0)
    else:
        # decouple from parent envronment
        os.chdir('/')
        os.setsid()
        os.umask(0)

        # second fork
        pid = os.fork()
        if pid > 0:
            exit(0)
        else:
            sys.stdout.flush()
            sys.stderr.flush()

            si = open(os.devnull, 'r')
            so = open(os.devnull, 'a+')
            se = open(os.devnull, 'a+')

            os.dup2(si.fileno(), sys.stdin.fileno())
            os.dup2(so.fileno(), sys.stdout.fileno())
            os.dup2(se.fileno(), sys.stderr.fileno())

            with open("/workspace/nvidia-examples/cnn/nvutils/run/pid.txt", "a") as pid_file:
                pid_file.write(str(os.getpid()) + "\n")

            run()

if __name__ == '__main__':
    daemonize()

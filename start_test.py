#!/usr/bin/python
# -*- coding: utf-8 -*-
import paramiko
from threading import Thread
import time
import importlib
import socket
import sys
import getopt
host_name = socket.gethostname()
my_module = importlib.import_module(host_name+'_vm_ips')
node_ips = my_module.node_ips

command = 'fio -direct=1 -ioengine=libaio -bs=4k -size=30G -iodepth=128 -rw=randwrite ' \
          '-filename=/dev/vdb  -name=test'
command2 = 'fio -direct=1 -ioengine=libaio -bs=4k -size=30G -iodepth=128 -rw=randread ' \
           '-filename=/dev/vdb  -name=test'
user_name = 'root'
password = 'qwer1011'


def startTest(ip, w_sig):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, 22, user_name, password)
    print ip
    if w_sig > 0:
        stdin, stdout, stderr = ssh.exec_command(command)
    else:
        stdin, stdout, stderr = ssh.exec_command(command2)
    print stderr.read()
    print stdout.read()
    ssh.close()


def main(argv):
    write_sig = 0
    time_sleep = 60
    try:
        opts, args = getopt.getopt(argv, "hw:t:")
    except getopt.GetoptError:
        print 'usage:start_test -w <write_signal> -t <time to sleep>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-w':
            write_sig = int(arg)
        if opt == '-t':
            time_sleep = int(arg)
        if opt == '-h':
            print 'usage:start_test -w <write_signal> -t <time to sleep>'
            sys.exit()
    for ip in node_ips:
        t = Thread(target=startTest, args=(ip, write_sig))
        t.start()
        time.sleep(time_sleep)


if __name__ == "__main__":
    main(sys.argv[1:])

#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import getopt
from threading import Thread
import libvirt
import socket
import paramiko

user_name = 'root'
password = 'qwer1011'
fio_command1 = 'fio1'
fio_command2 = 'fio2'

def getIPAddresses():
    """
    get all vms' ip address
    :return: list of IP addresses
    """
    """
    cat /var/lib/libvirt/dnsmasq/default.leases
    import libvirt
    conn = libvirt.open('qemu+ssh://root@localhost/system')
    for lease in conn.networkLookupByName("my_network").DHCPLeases():
        print(lease)
    """
    conn = libvirt.open('qemu+ssh://root@localhost/system')
    ip_lists = conn.networkLookupByName("my_network").DHCPLeases()
    return ip_lists


def startFio(fio_num):
    ip_lists = getIPAddresses()
    if len(ip_lists) < fio_num:
        print "not enough hosts"
        sys.exit(2)
    for idx, ip in enumerate(ip_lists):
        if idx > fio_num:
            break
        t = Thread(target=fioThread, args=(ip,))
        t.start()


def fioThread(ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, 22, user_name, password)
    stdin, stdout, stderr = ssh.exec_command(fio_command1)
    stdin, stdout, stderr = ssh.exec_command(fio_command2)
    ssh.close()


def main(argv):
    fio_num = 0
    try:
        opts, args = getopt.getopt(argv, "hn:")
    except getopt.GetoptError:
        print 'usage:start_fio -i <fio_num>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-n':
            fio_num = int(arg)
        if opt == '-h':
            print 'usage:start_fio -i <fio_num>'
            sys.exit()
    if fio_num > 0:
        startFio(fio_num)
    else:
        print 'usage:start_fio -i <fio_num>'


if __name__ == "__main__":
    main(sys.argv[1:])

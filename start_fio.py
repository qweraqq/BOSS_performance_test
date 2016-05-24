#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import getopt
import thread
import libvirt
import socket
import paramiko


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
    pass


def startFio(fio_num):
    pass


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

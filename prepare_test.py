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
host_name = socket.gethostname()

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
    ret_val = []

    conn = libvirt.open('qemu+ssh://root@localhost/system')
    ip_lists = conn.networkLookupByName("default").DHCPLeases()
    for item in ip_lists:
        ip_candidate = item['ipaddr']
        ret = os.system("ping -c 1 %s > /dev/null 2>&1" % ip_candidate)
        if ret == 0:
            ret_val.append(item['ipaddr'])
    print "available ips:"
    print ret_val
    return ret_val


def cleanUp(ips):
    for ip in ips:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, 22, user_name, password)
        ssh.exec_command('pgrep fio | xargs kill -9')
        ssh.close()


def main():
    ips = getIPAddresses()
    with open(host_name+'_vm_ips.py', 'w') as f:
        f.write("""#!/usr/bin/python
# -*- coding: utf-8 -*-
""")
        f.write("""node_ips = [""")
        for ip in ips:
            f.write("""\"{0}\", """.format(ip))
        f.write("""]""")
    cleanUp(ips)

if __name__ == "__main__":
    main()

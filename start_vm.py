#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import getopt
import socket

host_name = socket.gethostname()
ip_addr = socket.gethostbyname(socket.gethostname())
pool_name = 'p1'

def createVirtXml(special_id):
    """
    :param special_id:
    :return: volume_name
    """
    # create a volume first
    volume_name = host_name+"_"+str(special_id)
    createBootVolume(volume_name)
    # write a virsh create xml file
    file_name = host_name+"_"+str(special_id)+".xml"
    f2 = open(file_name, 'w')
    xml_content = """<domain type="kvm">
    <name>{0}</name>
    <memory unit="MiB">1024</memory>
    <currentMemory unit="MiB">1024</currentMemory>
    <vcpu>1</vcpu>
    <os>
        <type arch="x86_64" machine="pc">hvm</type>
        <boot dev="hd" />
        <boot dev="cdrom" />
    </os>
    <features>
        <acpi />
        <apic />
        <pae />
    </features>
    <clock offset="localtime" />
    <on_poweroff>destroy</on_poweroff>
    <on_reboot>restart</on_reboot>
    <on_crash>destroy</on_crash>
    <devices>
        <disk type="network" device="disk">
            <driver name="qemu" type="raw" />
            <source protocol ="boss" name="boss:{4}/{1}" />
            <target dev="vda" bus="virtio" />
        </disk>
        <interface type='network'>
            <source network='default'/>
        </interface>
        <input type="mouse" bus="ps2" />
        <graphics type="vnc" port="{2}" autoport="no" listen="{3}" keymap="en-us" />
    </devices>
</domain>
    """.format(volume_name, volume_name, 5900+special_id, ip_addr, pool_name)
    f2.write(xml_content)
    f2.close()
    return volume_name


def createAttachXml(volume_name):
    file_name = volume_name+"_attach.xml"
    f2 = open(file_name, 'w')
    xml_content = """<disk type='network' device='disk'>
   <driver name='qemu' type='raw' cache='none'/>
   <source file='boss:{1}/{0}'/>
   <target dev='vdb'/>
</disk>
""".format(volume_name, pool_name)
    f2.write(xml_content)
    f2.close()
    return file_name


def createBlankVolume(vm_name):
    volume_name = vm_name+"_blank_volume"
    os.system("volume_create -p " + pool_name + "-v "+volume_name+" -s 20G")
    return volume_name


def createBootVolume(volume_name):
    # TODO: change centos7 to a valid volume name
    os.system("volume_copy -sp " + pool_name + " -sv centos7 -dp " + pool_name + " -dv "+volume_name)


def cleanUp():
    """
    first: virsh destroy all vms start with hostname
    second: volume_delete all volumes start with hostname
    maybe will use xargs
    :return:
    """
    # TODO
    os.system("virsh list | grep " +  host_name +
              " | awk '{print $2}' | xargs -n 1 virsh destroy")
    os.system("volume_list -p p1 | grep " + host_name +
              "| awk '{print $7}' | xargs -n 1 volume_delete -p " + pool_name + " -v")




def startVm(num_vm):
    cleanUp()
    for i in xrange(num_vm):
        volume_name = createVirtXml(i)
        os.system("virsh create "+volume_name+".xml")
        # attack blank volume
        """
        first step: create a blank volume
        second step: virsh attach (? need xml)
        """
        blank_volume_name = createBlankVolume(volume_name)
        attach_filename = createAttachXml(blank_volume_name)
        os.system("virsh attach-device "+volume_name+" "+attach_filename)


def main(argv):
    vm_num = 0
    try:
        opts, args = getopt.getopt(argv, "hn:")
    except getopt.GetoptError:
        print 'usage:start_vm -i <vm_num>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-n':
            vm_num = int(arg)
        if opt == '-h':
            print 'usage:start_vm -i <vm_num>'
            sys.exit()
    if vm_num > 0:
        startVm(vm_num)
    else:
        print 'usage:start_vm -i <vm_num>'


if __name__ == "__main__":
    main(sys.argv[1:])

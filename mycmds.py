#!/Users/rlaney/.virtualenvs/NetEngineerONE/bin/python

from __future__ import absolute_import, division, print_function

import netmiko
import json
import mytools
import os
import sys
import signal
#from trigger.netdevices import NetDevices

signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOError: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C


if len(sys.argv) < 3:
    sys

netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException)

username, password = mytools.get_creds()

with open('mydevices.json') as device_file:
    devices = json.load(device_file)

for device in devices:
    try:
        print('~'*79)
        print('Connecting to ', device['nodeName'])
        connection = netmiko.ConnectHandler(ip=device['ipv4'], device_type=device['platform'],
                                            username=username, password=password)
        print(connection.send_command('show clock'))
        connection.disconnect()
    except netmiko_exceptions as e:
        print('Failed on ', device['nodeName'], e)

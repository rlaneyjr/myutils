#!/Users/rlaney/.virtualenvs/NetEngineerONE/bin/python

from __future__ import absolute_import, division, print_function

from getpass import getpass
import signal
import sys
import time


sig1 = signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOError: Broken pipe
sig2 = signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C


def get_input(prompt=''):
    try:
        line = raw_input(prompt)
    except NameError:
        line = input(prompt)
    return line


def get_creds():
    ''' Prompts for, and returns, a username and password. '''
    username = get_input('Enter Username: ')
    password = None
    while not password:
        password = getpass()
        password_verify = getpass('Retype Password: ')
        if password != password_verify:
            print('Your passwords do not match.  Try again.')
            password = None
    return username, password


def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def write_host_file():
    '''
    Pulls the name and IP out of the JSON file and writes to host_file.txt.
    This file is ordered and formatted for use as a system host file.
    *** MUST HAVE DEVICES POPULATED PRIOR ***
    '''
    with open('host_file.txt', 'w') as host_file:
        dev_set = set()
        for dev in devices:
            dev_set = (dev['ip']), (dev['nodeName'])
            host_file.write(dev_set[0])
            host_file.write('\t\t\t')
            host_file.write(dev_set[1])
            host_file.write('\n')

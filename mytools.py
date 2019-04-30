#!/usr/local/bin/env python
#title			:mytools.py
#description	:Updates local MongoDB data from Opmantek and SNow CMDB
#author			:Ricky Laney
#date			:20171215
#version		:1.0
#usage			:python mytools.py or ./mytools.py
#notes			:
#python_version	:2.7.13
#==============================================================================

from __future__ import absolute_import, division, print_function

from getpass import getpass
#import logging
#import os
import signal
import sys
import time


sig1 = signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOError: Broken pipe
sig2 = signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C

#FORMAT1 = '%(asctime)s:%(name)s:%(message)s'
#FORMAT2 = '%(asctime)s: %(levelname)s: %(lineno)d: %(message)s'
#file_name =  os.path.basename(__file__).replace('.py', '.log')
#
#logging.basicConfig(filename=MY_REPOS, filemode='w',
#                    format=FORMAT, level=logging.INFO)
#
#logger = logging.getLogger(file_name)
#logger.setLevel(logging.DEBUG)
#
#formatter = logging.Formatter(FORMAT)
#
#file_handler = logging.FileHandler('sample.log')
#file_handler.setLevel(logging.ERROR)
#file_handler.setFormatter(formatter)
#
#stream_handler = logging.StreamHandler()
#stream_handler.setFormatter(formatter)
#
#logger.addHandler(file_handler)
#logger.addHandler(stream_handler)

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


def timerfunc(func):
    """A timer decorator
    """
    def function_timer(*args, **kwargs):
        """A nested function for timing other functions
        """
        start = time.time()
        value = func(*args, **kwargs)
        end = time.time()
        runtime = end - start
        msg = "The runtime for {func} took {time} seconds to complete"
        print(msg.format(func=func.__name__, time=runtime))
        return value
    return function_timer


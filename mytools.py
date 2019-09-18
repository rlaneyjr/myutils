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
import os
import signal
import sys
from subprocess import getoutput
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


def select_editor(file_to_edit, lineno=0):
    # Choices to open the file with.
    CHOICES = """
            0) None
            1) Vim
            2) Sublime
            3) VSCode
            4) PyCharm
            5) MacVim
            """
    choice_map = {
            0: 'None',
            1: 'Vim',
            2: 'Sublime',
            3: 'VSCode',
            4: 'PyCharm',
            5: 'MacVim'
    }
    _cwd = os.getcwd()
    print(CHOICES)
    # grab the line number after header while the user is thinking
    with open(file_to_edit, 'r') as f:
        lines = f.readlines()
        lineno = len(lines)
    editor = get_input("Select a number: ")
    if not editor or editor == "0":
        exit()
    elif editor == "1":
        os.system(f"vim +{lineno} {file_to_edit}")
        exit()
    elif editor == "2":
        os.system(f"subl -n -a {_cwd} {file_to_edit}")
        exit()
    elif editor == "3":
        os.system(f"code -n -a {_cwd} -g {file_to_edit}:{lineno}")
        exit()
    elif editor == "4":
        os.system(f"charm {_cwd} {file_to_edit}:{lineno}")
        exit()
    elif editor == "5":
        os.system(f"mvim +{lineno} {file_to_edit}")
        exit()
    elif editor == "6":
        os.system(f"atom -n {file_to_edit}")
        exit()
    else:
        os.system("clear")
        print("\nI do not understand your answer.\n")
        print("Press <Ctrl + C> to quit.\n")
        return select_editor()


#!/usr/bin/env python
# -*- coding: utf-8 -*-

#title:             myspinner2.py
#description:       My CLI Spinner
#author:            Ricky Laney
#date:              20190118
#version:           0.0.1
#usage:             python myspinner2.py or ./myspinner2.py
#notes:             
#python_version:    3.6.5
#==============================================================================

import itertools
import sys
import time
import threading


class Spinner(object):
    spinner_cycle = itertools.cycle(['-', '/', '|', '\\'])

    def __init__(self):
        self.stop_running = threading.Event()
        self.spin_thread = threading.Thread(target=self.init_spin)

    def start(self):
        self.spin_thread.start()

    def stop(self):
        self.stop_running.set()
        self.spin_thread.join()

    def init_spin(self):
        while not self.stop_running.is_set():
            sys.stdout.write(next(self.spinner_cycle))
            sys.stdout.flush()
            time.sleep(0.25)
sys.stdout.write('\b')

# myspinner2.py Usage:
# --------------------
# def do_work():
#     time.sleep(3)
# 
# print 'starting work'    
# 
# spinner = Spinner()
# spinner.start()
# 
# do_work()
# 
# spinner.stop()
# print 'all done!'

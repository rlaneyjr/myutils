#!/usr/bin/env python

#title:             file_renamer.py
#description:       Remove those pesky file names that special characters.  Causes issues with Dropbox, OneDrive, etc.
#author:            Ricky Laney
#date:              20190430
#version:           0.1.1
#usage:             python file_renamer.py or ./file_renamer.py
#notes:             
#python_version:    3.7.0
#==============================================================================

import os
import sys
import re
from mytools import get_input

sp_chars = [ ':', ';', '{', '}', '[', ']', '|', '<', '>', ',', '?', '"', "'",
             '~', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')' ]

def get_dir(dir_argv=None):
    if dir_argv is None:
        location = get_input("Please enter the full path to the directory you wish to normalize the file/dir names: ")
        if os.path.exists(location):
            return location
        else:
            return False
    elif os.path.exists(dir_argv):
        return dir_argv
    else:
        return False


def get_names(the_dir):
    if os.path.exists(the_dir):
        results = []
        for pth, dnames, fnames in os.walk(the_dir):
            for fname in fnames:
                for spc in sp_chars:
                    if fname.__contains__(spc):
                        new_name = fname.replace(spc, '')
                        results.append({ 'old': os.path.join(pth, fname),
                                         'new': os.path.join(pth, new_name) })
            for dname in dnames:
                for spc in sp_chars:
                    if dname.__contains__(spc):
                        new_dir = dname.replace(spc, '')
                        results.append({ 'old_dir': os.path.join(pth, dname),
                                         'new_dir': os.path.join(pth, new_dir) })
        return results


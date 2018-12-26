#!/usr/bin/env python
# Copyright (c) 2010-2018 Network Engineering ONE Source
# Come visit us at https://netengone.com
#
# This software is provided under under a slightly modified version
# of the Apache Software License. See the accompanying LICENSE file
# for more information.
#

import datetime as dt
from functools import wraps
import logging
import logging.config
import os
import signal
import sys
import warnings

# Stops the ugly errors when hitting 'Ctrl+C'
signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOError: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C

FORMAT = '%(asctime)s: %(levelname)s: %(lineno)d: %(message)s'
FORMAT1 = '%(asctime)s:%(name)s:%(message)s'

#log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)

tday = dt.date.today().strftime('%m-%d-%Y')
log_dir = '/Users/rlaney/Logs/'
log_suffix = '.log'
log_prefix = str(os.path.basename(__file__)).split('.')[0]
log_name = "{}_{}{}".format(log_prefix, tday, log_suffix)
log_file = log_dir + log_name
no_files = str(len([n for n in os.listdir(log_dir) if n == log_name]))

if not os.path.exists(log_file):
    log_file = log_file
else:
    log_file = log_prefix + tday + '_' + no_files + log_suffix


class LogWith(object):
    '''Logging decorator that allows you to log with a specific logger.
    '''
    # Customize these messages
    ENTRY_MESSAGE = 'Entering {} at {}'
    EXIT_MESSAGE = 'Exiting {} at {}'

    def __init__(self, logger=None):
        self.logger = logging.getLogger(logger)
        self.logger = logging.basicConfig(filename=log_file, filemode='w',
                                          format=FORMAT, level=logging.INFO)

    def __call__(self, func):
        '''Returns a wrapper that wraps func.
        The wrapper will log the entry and exit points of the function
        with logging.INFO level.
        '''
        if not self.logger:
            try:
                self.logger = logging.getLogger(os.path.basename(__file__))
            except:
                self.logger = logging.getLogger(func.__module__)

        @wraps(func)
        def wrapper(*args, **kwds):
            start_time = dt.datetime.now()
            self.logger.info(self.ENTRY_MESSAGE.format(func.__name__, start_time))
            f_result = func(*args, **kwds)
            end_time = dt.datetime.now()
            self.logger.info(self.EXIT_MESSAGE.format(func.__name__, end_time))
            self.logger.info("FUNC: {} TIME: {}".format(func.__name__,
                                                      (end_time - start_time)))
            return f_result
        return wrapper


def log_event(event, objectid_attr=None, objectid_param=None):
    #Decorator to send events to the event log
    #You must pass in the event name, and may pass in some method of
    #obtaining an objectid from the decorated function's parameters or
    #return value.
    #objectid_attr: The name of an attr on the return value, to be
    #    extracted via getattr().
    #objectid_param: A string, specifies the name of the (kw)arg that
    #    should be the objectid.
    def wrap(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            self = extract_param_by_name(f, args, kwargs, 'self')
            value = f(*args, **kwargs)
            if objectid_attr is not None:
                event_objectids = getattr(value, objectid_attr)
            elif objectid_param is not None:
                event_objectids = extract_param_by_name(f, args, kwargs, objectid_param)
            else:
                event_objectids = None
            self._log_event(event, event_objectids)
            return value
        return decorator
    return wrap


class Logger(logging.getLoggerClass()):
    """Logger class for muliple thread logging.

    It writes debug messages to the file.

    :rtype: :class:`logging.RootLogger`
    :return: Configured logger object.
    """

    def __init__(self, name=None, log_level=None, log_dir=None):

        self.date_format = '%H:%M:%S'
        self.log_level = log_level
        self.name = name

        self.file_log_format = '%(asctime)s %(levelname)s %(filename)s' \
                               '[%(lineno)d] %(funcName)s: ' \
                               '%(message)s'

        self.log_name = self.name
        default_log_dir = os.path.join(self.get_log_dir(), self.name)
        self.log_dir = log_dir if log_dir else default_log_dir
        self.log_file = os.path.join(self.log_dir, self.log_name)

        # Configure the logger
        self.configure()

    def __get__(self):
        return self

    def configure(self):
        """Configure the logger object."""

        # Use specified log_dir or the default one
        self.create_dir(self.log_dir)

        # Create handlers
        file_handler = logging.FileHandler(self.log_file, mode='a')

        # Create formatters
        file_log_format = logging.Formatter(fmt=self.file_log_format,
                                            datefmt=self.date_format)

        # Attach formatters
        file_handler.setFormatter(file_log_format)

        # Create logger
        logging.Logger.__init__(self, self.log_name, level=self.log_level)

        # Configure logging level
        self.setLevel(self.log_level)
        file_handler.setLevel(self.log_level)

        # Attach handlers
        self.addHandler(file_handler)
        logging.getLogger('').addHandler(file_handler)

    def get_log_dir(self):
        """Return logging directory based on syetem platform.

        Default: /var/log

        :rtype: str
        :return: Path to log directory
        """

        for dirname in os.scandir():
            if dirname in ['Log', 'log', 'Logs', 'logs']:
                log_dir = {'darwin': dirname}
            else:
                log_dir = {'darwin': '~/Logs'}
        result = log_dir.get(sys.platform, '/var/log')
        return os.path.expanduser(result)

    def create_dir(self, name):
        """Recursively creates directores if it doesn't exist

        :type: str
        :param: The directory three path
        """

        if not os.path.exists(name):
            os.makedirs(name)

#!/usr/bin/env python
# Copyright (c) 2010-2018 Network Engineering ONE Source
# Come visit us at https://netengone.com
#
# This software is provided under under a slightly modified version
# of the Apache Software License. See the accompanying LICENSE file
# for more information.
#

import datetime
from functools import wraps
import logging
import os
import signal
import sys
import warnings

# How to import tqdm without enforcing it as a dependency
try:
    from tqdm import tqdm
except ImportError:

    def tqdm(*args, **kwargs):
        if args:
            return args[0]
        return kwargs.get('iterable', None)


# Stops the ugly errors when hitting 'Ctrl+C'
signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOError: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C

FILE_FMT = '%(asctime)s.%(msecs)03d: %(name)-12s: %(levelname)-8s: %(lineno)5d: %(funcName)s: %(message)s'
FILE_DATE_FMT = '%m-%d-%Y %H:%M:%S'
CONS_FMT = '%(asctime)s %(name)s %(message)s'
CONS_DATE_FMT = '%H:%M:%S'

#log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)


class TqdmLoggingHandler(logging.Handler):
    """ Custom Log Handler for use with TQDM
    """
    def __init__(self, level = logging.NOTSET):
        super(self.__class__, self).__init__(level)

    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.write(msg)
            self.flush()
        except (KeyboardInterrupt, SystemExit) as exc:
            raise exc
        except:
            self.handleError(record)


class LogWith:
    '''Logging decorator that allows you to log with a specific logger.
    '''
    # Customize these messages
    ENTRY_MESSAGE = 'Entering {} at {}'
    EXIT_MESSAGE = 'Exiting {} at {}'

    def __init__(self, logger=None):
        if os.environ.get('DEBUG', None):
            self.level = logging.DEBUG
        else:
            self.level = logging.INFO
        if logger is not None:
            self.logger = logging.getLogger(logger)
        else:
            try:
                self.logger = logging.getLogger(os.path.basename(__file__))
            except:
                self.logger = logging.getLogger(func.__module__)
        to_file = logging.FileHandler(self.get_log_file(), 'w')
        to_file.setLevel(self.level)
        file_fmt = logging.Formatter(FILE_FMT, FILE_DATE_FMT)
        to_file.setFormatter(file_fmt)

        to_console = logging.StreamHandler()
        to_console.setLevel(logging.WARN)
        con_fmt = logging.Formatter(CONS_FMT, CONS_DATE_FMT)
        to_console.setFormatter(con_fmt)
        # add the handlers to the logger
        self.logger.addHandler(to_console)
        self.logger.addHandler(to_file)

    def __call__(self, func):
        '''Returns a wrapper that wraps func.
        The wrapper will log the entry and exit points of the function
        with logging.INFO level.
        '''
        @wraps(func)
        def wrapper(self, *args, **kwds):
            start_time = datetime.datetime.now()
            self.logger.info(self.ENTRY_MESSAGE.format(func.__name__, start_time))
            f_result = func(*args, **kwds)
            end_time = datetime.datetime.now()
            self.logger.info(self.EXIT_MESSAGE.format(func.__name__, end_time))
            self.logger.info("FUNC: {} TIME: {}".format(func.__name__,
                                                        (end_time - start_time)))
            return f_result
        return wrapper

    def get_log_file(self):
        tday = datetime.date.today().strftime('%m-%d-%Y')
        log_dir = self.create_dir(self.get_log_dir())
        log_suffix = '.log'
        if self.logger.name:
            log_prefix = self.logger.name
        else:
            log_prefix = os.path.basename(__file__).split('.')[0]
        log_name = f"{log_prefix}_{tday}{log_suffix}"
        no_files = str(len([n for n in os.listdir(log_dir) if n == log_name]))
        log_file = os.path.join(log_dir, log_name)
        if os.path.exists(log_file):
            log_name = f"{log_prefix}_{tday}_{no_files}{log_suffix}"
        return os.path.join(log_dir, log_name)

    def get_log_dir(self):
        """Return logging directory based on environment or project.
        Default: /var/log
        :rtype: str
        :return: Path to log directory
        """
        if os.getenv('LOG_DIR', None):
            print(os.getenv('LOG_DIR'))
            return os.getenv('LOG_DIR')
        if os.getenv('PROJECT_DIR', None):
            return os.path.join(os.getenv('PROJECT_DIR'), 'Logs')
        else:
            for dirname in os.scandir(os.getcwd()):
                if dirname in ['Logs', 'logs', 'Log', 'log']:
                    return os.path.join(os.getcwd(), dirname)
                elif os.path.isdir(os.path.expanduser('~/Logs')):
                    return os.path.expanduser('~/Logs')
                else:
                    return '/var/log'

    def create_dir(self, name):
        """Recursively creates directores if it doesn't exist
        :type: str
        :param: The directory three path
        """
        if not os.path.exists(name):
            os.makedirs(name)


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
        stream_handler = logging.StreamHandler()
        # Create formatters
        file_formatter = logging.Formatter(fmt=self.file_log_format,
                                            datefmt=self.date_format)
        # Attach formatters
        file_handler.setFormatter(file_formatter)
        # Create logger
        logging.Logger.__init__(self, self.log_name, level=self.log_level)
        # Configure logging level
        self.setLevel(self.log_level)
        file_handler.setLevel(self.log_level)
        # Attach handlers
        self.addHandler(file_handler)
        logging.getLogger('').addHandler(file_handler)

    def get_log_dir(self):
        """Return logging directory based on environment or project.
        Default: /var/log
        :rtype: str
        :return: Path to log directory
        """
        if os.getenv('LOG_DIR', None):
            return os.getenv('LOG_DIR')
        if os.getenv('PROJECT_DIR', None):
            return os.path.join(os.getenv('PROJECT_DIR'), 'Logs')
        else:
            for dirname in os.scandir(os.getcwd()):
                if dirname in ['Logs', 'logs', 'Log', 'log']:
                    return os.path.join(os.getcwd(), dirname)
                elif os.path.isdir(os.path.expanduser('~/Logs')):
                    return os.path.expanduser('~/Logs')
                else:
                    return '/var/log'

    def create_dir(self, name):
        """Recursively creates directores if it doesn't exist
        :type: str
        :param: The directory three path
        """
        if not os.path.exists(name):
            os.makedirs(name)


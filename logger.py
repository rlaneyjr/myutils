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
import os
import signal
import sys

# Stops the ugly errors when hitting 'Ctrl+C'
signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOError: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C

FORMAT = '%(asctime)s: %(levelname)s: %(lineno)d: %(message)s'
FORMAT1 = '%(asctime)s:%(name)s:%(message)s'

logging.basicConfig(filename=log_file, filemode='w',
        format=FORMAT, level=logging.INFO)
logger = logging.getLogger('repo_up')

#log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)


class Logger(logging.getLoggerClass()):
    """Logger class for muliple thread logging.
    It writes debug messages to the file.
    :rtype: :class:`logging.RootLogger`
    :return: Configured logger object.
    """
    def __init__(self, name=None, log_level=None, log_dir=None):
        self.date_format = '%H:%M:%S'
        self.log_level = log_level
        self.file_log_format = '%(asctime)s %(levelname)s %(filename)s' \
                '[%(lineno)d] %(funcName)s: ' \
                '%(message)s'
        # Use specified filename or the default one
        default_name = dt.date.today().strftime('%m-%d-%Y')
        self.name = name if name else default_name
        self.log_name = self.name
        # Use specified log_dir or the default one
        default_log_dir = os.path.join(self.get_log_dir(), self.log_name)
        self.log_dir = log_dir if log_dir else default_log_dir
        self.log_file = get_log_file()
        # Configure the logger
        self.configure()

    def __get__(self):
        return self

    def configure(self):
        """Configure the logger object."""
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

    def get_log_file(self):
        """Returns the requested filename or tries to determine the best name
        by using the executed filename or function name. Fallsback to a date
        time formated filename.
        """
        log_end = '.log'
        log_start = self.log_name
        l_name = log_start + log_end
        l_file = os.path.join(self.log_dir, l_name)
        if not os.path.exists(l_file):
            return l_file
        else:
            num = str(len([n for n in os.listdir(self.log_dir) if n == l_name]))
            l_name = log_start + '_' + num + log_end
            return os.path.join(self.log_dir, l_name)


    def get_log_dir(self):
        """Return logging directory based on system platform.
        Default: /var/log
        :rtype: str
        :return: Path to log directory
        """
        log_dir = {'darwin': '~/Logs'}
        result = log_dir.get(sys.platform, '/var/log')
        return self.create_dir(os.path.expanduser(result))

    def create_dir(self, name):
        """Recursively creates directores if it doesn't exist
        :type: str
        :param: The directory three path
        """
        if not os.path.exists(name):
            os.makedirs(name)


class log_with(object):
    '''Logging decorator that allows you to log with a specific logger.
    '''
    # Customize these messages
    ENTRY_MESSAGE = 'Entering {} at {}'
    EXIT_MESSAGE = 'Exiting {} at {}'

    #logger = logging.getLogger(__name__)
    #logger.setLevel(logging.INFO)
    #formatter = logging.Formatter(FORMAT, filemode='w')


    def __init__(self, logger=None):
        self.logger = logger

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
            tday = dt.date.today().strftime('%m-%d-%Y')
            log_dir = '/Users/rlaney/Logs/'
            log_suffix = '.log'
            log_prefix = str(func.__name__)
            log_name = "{}_{}{}".format(log_prefix, tday, log_suffix)
            log_file = log_dir + log_name
            no_files = str(len([n for n in os.listdir(log_dir) if n == log_name]))
            if not os.path.exists(log_file):
                log_file = log_file
            else:
                log_file = log_prefix + tday + '_' + no_files + log_suffix
            logging.basicConfig(filename=log_file, filemode='w',
                                format=FORMAT, level=logging.INFO)
            start_time = dt.datetime.now()
            self.logger.info(self.ENTRY_MESSAGE.format(func.__name__, start_time))
            f_result = func(*args, **kwds)
            end_time = dt.datetime.now()
            self.logger.info(self.EXIT_MESSAGE.format(func.__name__, end_time))
            self.logger.info("FUNC: {} TIME: {}".format(func.__name__,
                                                      (end_time - start_time)))
            return f_result
        return wrapper


'''
if __name__ == '__main__':
    logging.basicConfig()
    log = logging.getLogger('custom_log')
    log.setLevel(logging.DEBUG)
    log.info('ciao')

    @log_with(log)     # user specified logger
    def foo():
        print 'this is foo'
    foo()

    @log_with()        # using default logger
    def foo2():
        print 'this is foo2'
    foo2()

# Example usage: @log_and_time("my_tag")
def log_and_time(tag):
    def log_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwds):
            start_time = dt.now()
            logger.info(ENTRY_MESSAGE.format(func.__name__))  # logging level .info(). Set to .debug() if you want to
            f_result = func(*args, **kwds)
            logger.info(EXIT_MESSAGE.format(func.__name__))   # logging level .info(). Set to .debug() if you want to
            end_time = datetime.now()
            return f_result

            try:
                log_info = function()
            except Exception as e:
                scrape_log.error = True
                scrape_log.error_message = e.message

        return wrapper
    return log_decorator #returning the decorator function


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


class MyLogger(logging.Formatter):
  #Prefixing logged messages with the function name.
  def __init__(self):
      logging.Formatter.__init__(self,'%(bullet)s %(message)s', None)

  def format(self, record):
    if record.levelno == logging.INFO:
      record.bullet = '[*]'
    elif record.levelno == logging.DEBUG:
      record.bullet = '[+]'
    elif record.levelno == logging.WARNING:
      record.bullet = '[!]'
    else:
      record.bullet = '[-]'

    return logging.Formatter.format(self, record)

def init():
    # We add a StreamHandler and formatter to the root logger
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(ImpacketFormatter())
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)
'''

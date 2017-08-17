# -*- coding: utf-8 -*-

import sys
sys.path.append('../')
sys.path.append('../queue')
sys.path.append('../browser_interface')

import logging
from logging import Handler
from logging.handlers import TimedRotatingFileHandler
# from queue import QueueFactory
import socket
import datetime

ERROR = 40
INFO = 20
DEBUG = 10

console_format = '%(asctime)s %(filename)s[line:%(lineno)d] %(funcName)s %(levelname)s %(message)s'
file_format = '%(asctime)s %(filename)s[line:%(lineno)d] %(funcName)s %(levelname)s %(message)s'
queue_format = '%(message)s'


class QueueHandler(Handler):

    def __init__(self, **kwargs):
        Handler.__init__(self)
        self.app = kwargs['app']
        self.queue = QueueFactory.QueueFactory().create(kwargs['type'], kwargs['queue_name'],
                                                        host=kwargs['host'], port=kwargs['port'])

    def emit(self, record):
        msg = self.format(record)
        data = {
            'host': socket.gethostname(),
            'app': self.app,
            'level': record.levelname,
            'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3],
            'msg': msg
        }
        self.queue.put(data)


class Logging():
    def __init__(self, name, console_level=DEBUG, file_level=INFO, queue_level=INFO,
                 console_format=console_format, queue_format=queue_format, file_format=file_format,
                 to_console=True, to_file=True, to_queue=False,
                 app=None, queue_type='QueueKafka', queue_name='log',
                 host='web14', port=51092, **kwargs):

        self.name = name
        self.__log = logging.getLogger('BBD')
        self.__log.setLevel(DEBUG)
        if to_console:
            self.__log.addHandler(self.get_console_handler(console_level, console_format))
        if to_file:
            self.__log.addHandler(self.get_file_handler(file_level, file_format))
        if to_queue:
            queue_config = {
                'app': app,
                'type': queue_type,
                'queue_name': queue_name,
                'host': host,
                'port': port
            }
            self.__log.addHandler(self.get_queue_handler(queue_level, queue_format, **queue_config))



    def get_console_handler(self, level, format):
        consolehandler = logging.StreamHandler()
        consolehandler.setLevel(level)
        formatter = logging.Formatter(format)
        consolehandler.setFormatter(formatter)
        return consolehandler


    def get_file_handler(self, level, format):
        filehandler = TimedRotatingFileHandler(self.name, when='D', interval=1, backupCount=5)
        filehandler.setLevel(level)
        filehandler.suffix = '%Y%m%d.log'
        formatter = logging.Formatter(fmt=format, datefmt='%Y-%m-%d %H:%M:%S')
        filehandler.setFormatter(formatter)
        return filehandler


    def get_queue_handler(self, level, format, **config):
        queuehandler = QueueHandler(**config)
        queuehandler.setLevel(level)
        formatter = logging.Formatter(format)
        queuehandler.setFormatter(formatter)
        return queuehandler


    def get_logging(self):
        return self.__log






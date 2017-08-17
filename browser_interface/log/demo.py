# -*- coding: utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from Logging import Logging

if __name__ == '__main__':
    log = Logging('BBDSpider').get_logging()
    log.debug('this is debug message')
    log.info('this is info message')
    log.error('this is error message')

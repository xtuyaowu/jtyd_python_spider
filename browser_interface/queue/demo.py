# -*- coding: utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from QueueFactory import QueueFactory

if __name__ == '__main__':
    # 1 new factory object
    factory = QueueFactory()

    # 2 create object
    queue = factory.create('QueueMongoDB', 'test_2', host='localhost', port=27017)
    # queue = factory.create('QueueSSDB', 'test', host='spider5', port=57888)
    # queue = factory.create('QueueKafka', 'test', host='web14', port=51092)

    # 3 operate
    print 'ssssssssssssss'
    queue.put({'_id':'ssd3a','name':'zhaosi'})
    print queue.size()
    print queue.get()



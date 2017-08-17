# -*- coding: utf-8 -*-

import QueueBase
from kafka import KafkaClient, SimpleConsumer, SimpleProducer, common
from Queue import Queue
import json


class QueueKafka(QueueBase.QueueBase):
    @QueueBase.catch
    def __init__(self, name, host='web14', port=51092, **kwargs):
        QueueBase.QueueBase.__init__(self, name, host, port)
        self.__queue = []
        self.__kafka = KafkaClient('%s:%d' % (host, port))
        self.__producer = SimpleProducer(self.__kafka, async=kwargs.get('async', False))
        self.__producer.client.ensure_topic_exists(self.name)
        self.__consumer = SimpleConsumer(self.__kafka, self.name + '_consumer', self.name, auto_commit_every_n=1)

    def __del__(self):
        if self.__kafka:
            [self.put(x.message.value) for x in self.__queue]
            self.__kafka.close()

    @QueueBase.catch
    def put(self, value, *args, **kwargs):
        if isinstance(value, dict) or isinstance(value, list):
            self.__producer.send_messages(self.name, json.dumps(value))
        else:
            self.__producer.send_messages(self.name, value.encode('utf-8') if isinstance(value, unicode) else value)

    @QueueBase.catch
    def get(self, *args, **kwargs):
        if not self.__queue:
            self.__consumer._fetch()
            kq = self.__consumer.queue
            while not kq.empty():
                partition, result = kq.get_nowait()
                self.__queue.append(result)
                self.__consumer.offsets[partition] += 1
                self.__consumer.count_since_commit += 1
            self.__consumer.queue = Queue()
            self.__consumer.commit()
        return self.__queue.pop().message.value if self.__queue else None

    @QueueBase.catch
    def size(self, *args, **kwargs):
        count = 0
        for k, v in self.__consumer.offsets.items():
            reqs = [common.OffsetRequest(self.name, k, -1, 1)]
            (resp, ) = self.__consumer.client.send_offset_request(reqs)
            count += (resp.offsets[0] - v)
        return count + len(self.__queue)

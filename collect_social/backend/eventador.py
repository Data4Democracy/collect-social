from pykafka import KafkaClient
from pykafka.common import OffsetType
import json
import uuid

class EventadorClient:
    def __init__(self, config):
        self.config = config
        self.client = KafkaClient(hosts=config.get('broker'))
        self.topic = self.client.topics[config.get('topic')]

    def get_topic_list(self):
        return self.client.topics

    def produce(self, producer, payload):
        data = json.dumps(payload.get('value')).encode('utf-8')
        producer.produce(message=data,
                         partition_key=payload.get('key', bytes(1)))

    async def produce_one(self, payload, topic=None):
            t = await self.resolve_topic(topic)
            with t.get_producer(min_queued_messages=1, linger_ms=0) as producer:
                self.produce(producer, payload)

    async def produce_many(self, payloads, topic=None, log=True):
        t = await self.resolve_topic(topic)
        with t.get_producer(delivery_reports=log, linger_ms=0) as producer:
            for payload in payloads:
                self.produce(producer, payload)

    async def resolve_topic(self, topic):
        if topic is not None:
            return self.client.topics.get(topic.encode)
        else:
            return self.topic

    def consume(self, offset_type):
        consumer = self.topic.get_simple_consumer(auto_offset_reset=offset_type,
                                                  consumer_group=uuid.uuid4().bytes,
                                                  reset_offset_on_start=True)
        for message in consumer:
            yield message

    def consume_all(self):
        return self.consume(OffsetType.EARLIEST)

    def consume_latest(self):
        return self.consume(OffsetType.LATEST)

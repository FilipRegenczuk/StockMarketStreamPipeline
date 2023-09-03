import json
from kafka import KafkaProducer

class StockDataProducer:
    def __init__(self, broker: str, topic: str):
        self.broker = broker
        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=self.broker,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all',
            # compression_type='snappy',
            # batch_size=
            retries=3
        )
    
    def send_message(self, msg: str):
        print("sending message ...")
        try:
            self.producer.send(self.topic, msg)
            self.producer.flush()
            print("message send successfully")
            return 
        except Exception as ex:
            return ex


producer = StockDataProducer('127.0.0.1:9092', 'python-test')
data = {'part1': 'hello', 'part2': 'world'}
resp = producer.send_message(data)
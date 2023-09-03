import json
import time
from stock_data_generator import StockDataGenerator
from stock_data_producer import StockDataProducer

class StockDataSimulator:

    def __init__(self):
        self.config = StockDataSimulator.get_config()
        self.generator = StockDataGenerator(
            action=self.config.get('stockActionName')
        )
        self.producer = StockDataProducer(
            broker=self.config.get('bootstrapServers'),
            topic=self.config.get('kafkaTopic')
        )
    
    def simulate(self):
        data = self.generator.get_historical_data(period=self.config.get('period'))
        for _, record in data.iterrows():
            self.producer.send_message(msg=dict(record))
            time.sleep(1/self.config.get('simulationRatePerSec'))


    @staticmethod
    def get_config():
        with open('config/parameters.json') as file:
            return json.load(file)


simulator = StockDataSimulator()
simulator.simulate()

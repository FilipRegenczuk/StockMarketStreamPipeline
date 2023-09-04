import json
import time
from pathlib import Path
from os.path import join
from stock_data_generator import StockDataGenerator
from stock_data_producer import StockDataProducer

class StockDataSimulator:
    """
    TODO add docstrings
    """
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
        config_path = join(Path(__file__).parent.parent, 'config/parameters.json')
        try:
            with open(config_path) as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Config file not found on path {config_path}!")
            raise

if __name__ == '__main__':
    simulator = StockDataSimulator()
    simulator.simulate()

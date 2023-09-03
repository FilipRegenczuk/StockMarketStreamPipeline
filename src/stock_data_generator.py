import yfinance as yf
from os import makedirs, path


class StockDataGenerator:
    def __init__(self, action: str):
        self.ticker = yf.Ticker(action)
        self.action = action

    def get_historical_data(self, period: str='1y'):
        return self.ticker.history(period=period)

    def download_data(self, dir_path: str='./data', period: str='1y'):
        makedirs(dir_path, exist_ok=True)
        self.get_historical_data(period=period).to_json(
            path.join(dir_path, f'{self.action}.json'),
            orient='table',
            indent=4
        )


gen = StockDataGenerator('AAPL')
# print(gen.get_historical_data('1y'))
gen.download_data('data')

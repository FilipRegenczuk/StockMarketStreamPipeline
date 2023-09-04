import yfinance as yf
from os import makedirs, path


class StockDataGenerator:
    """
    TODO add docstrings
    """
    def __init__(self, action: str):
        self.ticker = yf.Ticker(action)
        self.action = action

    def get_historical_data(self, period: str='1y'):
        data = self.ticker.history(period=period).reset_index()
        data['Id'] = self.action + data['Date'].dt.strftime(r'%Y%m%d').astype(str)
        data['Date'] = data['Date'].dt.strftime(r'%d/%m/%Y') # get rid of hours scope
        return data

    def download_data(self, dir_path: str='./data', period: str='1y'):
        makedirs(dir_path, exist_ok=True)
        self.get_historical_data(period=period).to_json(
            path.join(dir_path, f'{self.action}.json'),
            orient='table',
            indent=4
        )

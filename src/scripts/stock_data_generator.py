import yfinance as yf
from os import makedirs, path


class StockDataGenerator:
    """
    Class defines stock data generator, which task is to download historical
    data for a specified action from the Yahoo! Finance portal.

    Attributes
    ----------
    action : str
        Name of stock market action.

    Methods
    -------
    get_historical_data(period: str) 
        Returns action historical data for specified period. Method returns pandas
        DataFrame with additional column 'Id' (action name and datestamp).
    
    download_data(dir_path: str, period: str)
        Saves action historical data for specified period to JSON file.

    """
    def __init__(self, action: str):
        self.ticker = yf.Ticker(action)
        self.action = action

    def get_historical_data(self, period: str='1y'):
        data = self.ticker.history(period=period).reset_index()
        data['Id'] = self.action + data['Date'].dt.strftime(r'%Y%m%d').astype(str)
        data['Date'] = data['Date'].dt.strftime(r'%Y%m%d').astype(int) # get rid of hours scope
        return data

    def download_data(self, dir_path: str='./data', period: str='1y'):
        makedirs(dir_path, exist_ok=True)
        self.get_historical_data(period=period).to_json(
            path.join(dir_path, f'{self.action}.json'),
            orient='table',
            indent=4
        )

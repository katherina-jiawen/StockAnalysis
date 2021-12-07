from my_module import utils
from my_module import yahoo
from datetime import datetime


class Analysis():
    initial_cash = 1000000
    
    def __init__(self, code, start='2000-01-01', end=datetime.now()):
    
        """ 
        Parameters
        ----------
        code : string
            The stock string
        start : string 
            The starting date 
        end : string
            The ending date 
        """
    
        self.code = code
        self.start = start
        self.end = end
        # get data from yahoo.com
        self.df = yahoo.get_data_from_yahoo(code, start, end)

    

    def long_hold(self):
        
        """Calculate the annual return 
           Buy at begin, long hold 
            
        Returns
        -------
        ann_return : float
            The annual return of the stock
        """
        # Calculate return
        from_date = utils.timestamp_to_date(self.df.index[0].timestamp())
        end_date = utils.timestamp_to_date(self.df.index[-1].timestamp())
        years = utils.calculate_years(self.df.index[0], self.df.index[-1])
        total_return = (self.df.Close[-1] - self.df.Close[0]) / self.df.Close[0]
        ann_return = (total_return + 1) ** (1 / years) - 1
        ann_return_percentage = str(round(ann_return * 100, 2)) + '%'
        print(f'Long hold {self.code} from {from_date} to {end_date} annualized return is {ann_return_percentage}')
        return ann_return

    def use_ma_long(self, ma_length = 50):
        
        """Calculate the annal return when trade with respect to moving average. 
           If the closing price is higher than the price of moving average, buy with all cash;
           If the closing price is lower than the price of moving average, sell all stocks.
    
        Parameters
        ----------
        ma_length : int 
            The length of day for moving average. 
    
        Returns
        -------
        ma_length : int
             The length of day for moving average. 
        ann_return : float
            The annual return of the stock.
        """
            
        # Calculate moving average (Ma)
        self.df['Ma'] = self.df['Close'].rolling(ma_length).mean()
        # begin test
        cash = self.initial_cash
        stocks = 0
        for index, row in self.df.iterrows():
            #The first 49 days do not have MA
            if row['Ma']:
                if (row['Close'] > row['Ma']) and (stocks == 0):
                    # Buy stock when you don't have stock ，
                    # We assume we can use all the cash to buy the stocks. 
                    # The number of stock did not need to be the integer. 
                    stocks = cash / row['Close']
                    cash = 0
                if (row['Close'] < row['Ma']) and (stocks > 0):
                    # Sell stock
                    cash = stocks * row['Close']
                    stocks = 0

        # Calculate return
        from_date = utils.timestamp_to_date(self.df.index[0].timestamp())
        end_date = utils.timestamp_to_date(self.df.index[-1].timestamp())
        years = utils.calculate_years(self.df.index[0], self.df.index[-1])
        value = self.df.Close[-1] * stocks + cash
        total_return = (value - self.initial_cash) / self.initial_cash
        ann_return = (total_return + 1) ** (1 / years) - 1
        ann_return_percentage = str(round(ann_return * 100, 2)) + '%'
        print(f'Use {ma_length}days ma only buy {self.code} from {from_date} to {end_date} annualized return is {ann_return_percentage}')
        return ma_length, ann_return

    def use_ma_long_short(self, ma_length=50):
        
        """Calculate the annual return when trade with respect to moving average. 
           If the closing price is higher than the price of moving average, clear all short and buy.
           If the closing price is lower than the price of moving average, sell all stocks and short the stock.
    
        Parameters
        ----------
        ma_length : int 
            The length of day for moving average. 
    
        Returns
        -------
        ma_length : int
             The length of day for moving average. 
        ann_return : float
            The annual return of the stock.
        """
            
        # Calculate ma
        self.df['Ma'] = self.df['Close'].rolling(ma_length).mean()
        cash = self.initial_cash
        stocks = 0
        for index, row in self.df.iterrows():
            if row['Ma']:
                if (row['Close'] > row['Ma']) and (stocks <= 0):
                    # Clear the short
                    cash = cash + stocks * row['Close']
                    stocks = 0
                    # Buy stock
                    stocks = cash / row['Close']
                    cash = 0
                if (row['Close'] < row['Ma']) and (stocks >= 0):
                    # Clear the long
                    cash = cash + stocks * row['Close']
                    stocks = 0
                    # Short the stock
                    stocks = 0 - cash / row['Close']
                    cash = cash * 2

        # Calculate return
        from_date = utils.timestamp_to_date(self.df.index[0].timestamp())
        end_date = utils.timestamp_to_date(self.df.index[-1].timestamp())
        years = utils.calculate_years(self.df.index[0], self.df.index[-1])
        value = self.df.Close[-1] * stocks + cash
        total_return = (value - self.initial_cash) / self.initial_cash
        ann_return = (total_return + 1) ** (1 / years) - 1
        ann_return_percentage = str(round(ann_return * 100, 2)) + '%'
        print(f'Use {ma_length}days ma long and short {self.code} from {from_date} to {end_date} annualized return is {ann_return_percentage}')
        return ma_length, ann_return


from my_module import utils
from my_module import yahoo

class Analysis():
    initial_cash = 1000000

    def __init__(self, code, start='2000-01-01'):
        self.code = code
        self.start = start
        # get data from yahoo.com
        self.df = yahoo.get_data_from_yahoo(code, start)

    # buy at begin, long hold 长期持有
    def long_hold(self):
        # calculate return
        # find the initial public date of the stock.
        from_date = utils.timestamp_to_date(self.df.index[0].timestamp())
        years = utils.to_now_years(self.df.index[0])
        total_return = (self.df.Close[-1] - self.df.Close[0]) / self.df.Close[0]
        ann_return = (total_return + 1) ** (1 / years) - 1
        ann_return_percentage = str(round(ann_return * 100, 2)) + '%'
        print(
            'Long hold ' + self.code + ' from ' + from_date + ' to now annualized return is ' + ann_return_percentage)

    def use_ma_long(self, ma_length = 50):
        #全仓买入，如果跌了全仓卖 clear
        """
        Trade with the ma line, if the close bigger than ma buy and if the close lower than ma clear
        :param ma_length: the days of ma
        :return: (ma_length, annualized return)
        """
        # calculate moving average (Ma)
        self.df['Ma'] = self.df['Close'].rolling(ma_length).mean()
        # begin test
        cash = self.initial_cash
        stocks = 0
        for index, row in self.df.iterrows():
            #The first 49 days do not have MA
            if row['Ma']:
                if (row['Close'] > row['Ma']) and (stocks == 0):
                    # buy stock when you don't have stock ，
                    # HEre we assume we can use all the cash to buy the stock, 
                    #the numbero f stock did not need to be the integer. 
                    stocks = cash / row['Close']
                    cash = 0
                if (row['Close'] < row['Ma']) and (stocks > 0):
                    # sell stock
                    cash = stocks * row['Close']
                    stocks = 0

        # calculate return
        from_date = utils.timestamp_to_date(self.df.index[0].timestamp())
        years = utils.to_now_years(self.df.index[0])
        value = self.df.Close[-1] * stocks + cash
        total_return = (value - self.initial_cash) / self.initial_cash
        ann_return = (total_return + 1) ** (1 / years) - 1
        ann_return_percentage = str(round(ann_return * 100, 2)) + '%'
        print('Use ' + str(
            ma_length) + ' days ma only buy ' + self.code + ' from ' + from_date + ' to now annualized return is ' + ann_return_percentage)
        return ma_length, ann_return

    def use_ma_long_short(self, ma_length=50):
        """
        Trade with the ma line, if the close bigger than ma clear all short and buy
        and if the close lower than ma sell all stock and short the stock
        :param ma_length: the days of ma
        :return: (ma_length, annualized return)
        """
        # calculate ma
        self.df['Ma'] = self.df['Close'].rolling(ma_length).mean()
        cash = self.initial_cash
        stocks = 0
        for index, row in self.df.iterrows():
            if row['Ma']:
                if (row['Close'] > row['Ma']) and (stocks <= 0):
                    # clear the short
                    cash = cash + stocks * row['Close']
                    stocks = 0
                    # buy stock
                    stocks = cash / row['Close']
                    cash = 0
                if (row['Close'] < row['Ma']) and (stocks >= 0):
                    # clear the long
                    cash = cash + stocks * row['Close']
                    stocks = 0
                    # short
                    stocks = 0 - cash / row['Close']
                    cash = cash * 2

        # calculate return
        from_date = utils.timestamp_to_date(self.df.index[0].timestamp())
        years = utils.to_now_years(self.df.index[0])
        value = self.df.Close[-1] * stocks + cash
        total_return = (value - self.initial_cash) / self.initial_cash
        ann_return = (total_return + 1) ** (1 / years) - 1
        ann_return_percentage = str(round(ann_return * 100, 2)) + '%'
        print('Use ' + str(
            ma_length) + ' days ma long and short ' + self.code + ' from ' + from_date + ' to now annualized return is ' + ann_return_percentage)
        return ma_length, ann_return


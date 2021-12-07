import pandas_datareader as pdr
import datetime


def get_data_from_yahoo(code, start='2000-01-01', end=datetime.datetime.today()):
    
    """Get stock data from yahoo.com
    
    Parameters
    ----------
    code : string
        The code of the stock.
    start : string
        The beginning date of the data you want to use. 
        Defult : 2000-01-1
    end : string
        The ending date date of the data you want to use. 
        Defult: Today
    
    Returns
    -------
    _df : DataFrame
        Contains each stocks information day by day
        
    """
    
    _df = pdr.get_data_yahoo(code, start, end)
    _df.index.name = 'datetime'
    print(code, 'Get data successfully...')
    
    return _df

# Citation of pdr.get_data_yahoo() : 
# https://www.programcreek.com/python/example/92135/pandas_datareader.data.get_data_yahoo
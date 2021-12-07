import datetime   
import pandas
from my_module.utils import timestamp_to_date
from my_module.utils import calculate_years
from my_module.yahoo import get_data_from_yahoo
from my_module.analysis import Analysis

def test_timestamp_to_date():
    assert callable (timestamp_to_date)
    assert isinstance (timestamp_to_date(1638729026),str)
    assert timestamp_to_date(1638729026) == '2021-12-05'

def test_calculate_years():
    assert callable (calculate_years)
    start = datetime.datetime.strptime('2020-01-01', "%Y-%m-%d")
    end = datetime.datetime.strptime('2021-12-31', "%Y-%m-%d")
    assert isinstance(calculate_years(start, end), float)
    assert calculate_years(start, end) == 2.0

def test_get_data_from_yahoo():
    assert callable (get_data_from_yahoo)
    assert isinstance (get_data_from_yahoo ('AAPL', start='2000-01-01'),pandas.core.frame.DataFrame)
    

def test_long_hold():
    analysis = Analysis('AAPL', start='2000-01-01', end = '2010-01-01')
    assert callable(analysis.long_hold)
    assert isinstance (analysis.long_hold(),float)
    assert analysis.long_hold() == 0.2237172236920788

def test_use_ma_long():
    analysis = Analysis('AAPL', start='2000-01-01', end = '2010-01-01')
    assert callable(analysis.use_ma_long)
    assert isinstance (analysis.use_ma_long(),tuple)
    assert analysis.use_ma_long() == (50,0.25916164467810754)
    
def test_use_ma_long_short():
    analysis = Analysis('AAPL', start='2000-01-01', end = '2010-01-01')
    assert callable(analysis.use_ma_long_short)
    assert isinstance (analysis.use_ma_long_short(),tuple)                 
    assert analysis.use_ma_long_short() == (50,0.16047562628218426)
import datetime
import time


def calculate_years(start, end):
    
    """Calculate the years between the starting date and the ending date
    
    Parameters
    ----------
    start : string 
        The starting date 
    end : string
        The ending date
    
    Returns
    -------
    days : int 
        The days between the starting date and the ending date
    days/365 : int or float 
        The years between the starting date and the ending date
    """
    
    days = (end - start).days
    return days / 365


def timestamp_to_date(timestamp):

    """Change timestamp to data string.
    
    Parameters
    ----------
    timestamp : int or float
        The timestamp that needs to be converted.
    
    Returns
    -------
    date : string
        The date in the string format.
    """
        
    time_struct = time.localtime(timestamp)
    date = time.strftime('%Y-%m-%d', time_struct)
    return date
    
 #citation of time.strftime : https://www.programiz.com/python-programming/datetime/strftime





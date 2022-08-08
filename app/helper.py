import time
from datetime import datetime


import logging
logging.basicConfig(level='DEBUG')

def stringToTimestamp(string):
    element = datetime.strptime(string,"%d/%m/%Y")
    tuple = element.timetuple()
    timestamp = time.mktime(tuple)
    return timestamp


def timestampToString(timestamp):
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object